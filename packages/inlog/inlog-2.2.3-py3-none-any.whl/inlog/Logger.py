import sys
import configparser
import os
import __main__
import datetime
import hashlib
import warnings
from pathlib import Path
import json
import json
from inlog.Tree import TreeNode

class Logger(object):
    """Parser to read inputfiles and create logs."""

    def __init__(self, config_dict=None, version=None, def_opts=None):
        """
        Create Logger for config parsing and logging.

        Parameters
        ----------
        config_dict : dict
            Dictionary with the input parameters.
        version : str
            Version of the program.

        Keyword Arguments
        -----------------
        def_opts : dict, optional
            Dictionary with default input parameters. (default: None)
        """
        self.filename=None
        self.version=version
        self.creation_date=datetime.datetime.now()
        self.outfilenames=[]

        if config_dict is None:
            config_dict={} 
        if def_opts is None:
            def_opts={}
        self.options=TreeNode.from_leafdict(def_opts)
        config_tree=TreeNode.from_leafdict(config_dict)
        self.options.update(config_tree)
        self.accessed=self.options.copy()
        self.accessed.set_all(False)
    
    
    def _get(self, *keys):
        """Get the value of an option without setting it to accessed.

        Returns
        -------
        value
            The value of the option
        """
        return self.options.get(*keys).to_leafdict()
    
    def get(self, *keys):
        """Get the value of an input parameter. Mark this parameter as accessed.

        Parameters
        ----------
            *keys: The keys to the input parameter. If no keys are given, the whole parameter dictionary is returned.

        Returns
        -------
        value
            The value for the given keys.
        """
        return_value=self._get(*keys)
        self.set_accessed(*keys)
        return return_value

    def set(self, value, *keys):
        """Set the value of a parameter.

        Arguments:
            value: The value to be set.
            *keys: The keys to the parameter.
        """
        self.options.get(*keys).value=value
        self.options.make_leaf(*keys)
    
    def set_subtree(self, config_dict, *keys):
        """Set multiple options at once by providing a (nested) dictionary.

        Parameters
        ----------
        config_dict : dict
            The dictionary with the new options. Can be nested.
        *keys : tuple
            The keys to the subtree where the new options will be inserted.
        """
        subtree=TreeNode.from_leafdict(config_dict)
        self.options.get(*keys).children=subtree.children
        subtree_accessed=subtree.copy()
        subtree_accessed.set_all(True)
        self.accessed.get(*keys).children=subtree_accessed.children
    
    def _reset_access(self):
        """Reset the accessed status of all parameters."""
        self.accessed.set_all(False)
    
    # def _get_accessed(self, *keys):
    #     """Get the accessed subtree of a parameter."""
    #     if len(keys)==0:
    #         return self.accessed
    #     print("here")
    #     print(keys)
    #     print(self._get_accessed(*keys[:-1]))
    #     print(self._get_accessed(*keys[:-1])[keys[-1]])
    #     return self._get_accessed(*keys[:-1])[keys[-1]]
    
    def is_accessed(self, *keys):
        """Get the accessed status of a parameter."""
        return self.accessed.get(*keys).value
    
    def set_accessed(self, *keys):
        """Mark a parameter as accessed."""
        self.accessed.set_all(True, *keys)

    def get_accessed_options(self, *keys):
        """Get only the accessed parameters of a given subtree."""
        accessed_state=self.accessed.get(*keys).filter_any()
        if accessed_state is None:
            return None
        accessed_options=self.options.get(*keys)
        accessed_options=accessed_options.select(accessed_state)
        return accessed_options.to_leafdict()

    
    # def _find_depth_first(self, key, path=None):
    #     if path is None:
    #         path=[]
    #     subtree=self._get(*path)
    #     if isinstance(subtree, dict):
    #         for k, v in subtree.items():
    #             if k == key:
    #                 return path + [k]
    #             if isinstance(v, dict):
    #                 result = self._find_depth_first(key, path + [k])
    #                 if result is not None:
    #                     return result
    #     return None
    
    
    def __getitem__(self, keys):
        """Get the first matching parameter or subtree in the config dictionary.

        Parameters
        ----------
        *keys: str
            Keys matching the path to the parameter or subtree, in the order they appear in the path.
            For example, the keys (b,d) will match the paths a/b/c/d as well as a/b/d.
        Returns
        -------
        value
            The depth-first matching parameter or subtree.
        """
        if not isinstance(keys, tuple):
            keys=(keys,)
        result=self.options.match_depth_first(*keys)
        if result is None:
            raise KeyError(f"No matches for {keys} found.")
        self.accessed.match_depth_first(*keys).set_all(True)
        return result.to_leafdict()

    def __setitem__(self, keys, value):
        """Set the first matching parameter or subtree in the config dictionary.

        Parameters
        ----------
        keys: tuple
            Keys matching the path to the parameter or subtree, in the order they appear in the path.
            For example, the keys (b,d) will match the paths a/b/c/d as well as a/b/d.
        value: The value for the matching parameter or subtree.
        """
        if not isinstance(keys, tuple):
            keys=(keys,)
        result=self.options.match_depth_first(*keys)
        if result is None:
            raise KeyError(f"No matches for {keys} found.")
        result.value=value

    def convert_type(self, dtype, *keys):
        """
        Convert an input option from string to a given type.

        Parameters
        ----------
        dtype : function
            Type conversion function. Typical are int, float or Path. bool is also allowed.
        *keys : tuple
            The option keys to be converted. If a subtree is given, all options in the subtree are converted.
        
        Notes
        -----
        If `dtype` is `bool`, the conversion function will convert the string values "true", "yes", "1", and "t" to `True`, and all other values to `False`.
        """
        if dtype==bool:
            conversion_func=lambda val: val.lower() in ("true", "yes", "1", "t")
        else:
            conversion_func=dtype
        conversion_func_none=lambda val: conversion_func(val) if val is not None else None #non-leaf nodes always have value None
        self.options.get(*keys).map(conversion_func_none)

    def convert_array(self, dtype, *keys, sep=",", removeSpaces=False):
        """
        Convert one or multiple config options from string to an array of the given type.

        Parameters
        ----------
        dtype : type
            Type to convert the array element, e.g. str, int, float
        *keys : tuple
            The option keys to be converted. If a subtree is given, all options in the subtree are converted.

        Keyword Arguments
        -----------------
        sep : str, optional
            The separator between the array values (default: ',')
        removeSpaces : bool, optional
            Remove spaces in the elements when converting to string array. (default: False)
        """
        def convert_array_none(val):
            if val is None:
                return None
            elif isinstance(val, str):
                array=val.split(sep)
                if removeSpaces:
                    array=[x.strip() for x in array]
                array=[a for a in array if a]
                array=[dtype(a) for a in array]
                return array
            else:
                raise ValueError(f"Option {val} is not a string. Cannot convert to array.")
        self.options.get(*keys).map(convert_array_none)
    

    def add_outfile(self, output_files):
        """
            Add the given filename(s) to the list of outputfiles of your program. They will be listed in the logfile, together with their hash value.

            Parameters
            ----------
            output_files : str or Path or list
                The paths of the outputfiles. Relative paths will be interpreted relative to the current working directory.
            """
        if isinstance(output_files, str) or isinstance(output_files, Path):
            output_files=[output_files]
        output_files=[Path(p).resolve() for p in output_files]
        for path in output_files:
            if not path.exists():
                warnings.warn(f"At the moment, there is no such file: {path}")
            self.outfilenames.append(path)

    def set_outfile(self, output_files):
        """
        Set the given filename(s) as the list of outputfiles of your program. They will be listed in the logfile, together with their hash value.

        Parameters
        ----------
        output_files : str or list of str
            The paths of the outputfiles. Relative paths will be interpreted relative to the current working directory.
        """
        self.outfilenames=[]
        self.add_outfile(output_files)

    def hash_file(self, file):
        """
        Calculate the hash of a file.

        Parameters
        ----------
        file : str or Path
            The path of the file

        Returns
        -------
        str
            The hexadecimal sha256 hash of the file.
        """
        BLOCK_SIZE = 65536 # The size of each read from the file
        file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
        with open(file, 'rb') as f: # Open the file to read it's bytes
            fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
            while len(fb) > 0: # While there is still data being read from the file
                file_hash.update(fb) # Update the hash
                fb = f.read(BLOCK_SIZE) # Read the next block from the file
        return file_hash.hexdigest() # Get the hexadecimal digest of the hash

    def _get_program_file(self):
        try: #If the program is run from a script
            return __main__.__file__
        except AttributeError: 
            #there might be more options to try
            #see: https://stackoverflow.com/a/35514032
            return None
    
    def _to_string(self, accessed_only=False):
        lines=[]
        lines.append("<Date> "+str(datetime.datetime.now()))
        lines.append("<Program> "+str(self._get_program_file()))
        lines.append("<Arguments> "+str(sys.argv[1:]))
        lines.append("<Version> "+str(self.version))
        lines.append("<Input> "+str(self.filename))
        lines.append("<Runtime> "+str(datetime.datetime.now()-self.creation_date))
        lines.append("**************************")
        if accessed_only:
            log_options_dict=self.get_accessed_options()
        else:
            log_options_dict=self.options.to_leafdict()
        log_options_str=json.dumps(log_options_dict, indent=4, default=str)       
        lines+=[line for line in log_options_str.split("\n")]
        if len(self.outfilenames)>0:
            lines.append("**************************")
            lines.append("Output files created:")
            for path in self.outfilenames:
                lines.append("<PATH> "+str(path))
                lines.append("<HASH> "+self.hash_file(path))
        lines=[l+"\n" for l in lines]
        return lines

    def _create_log_txt(self, accessed_only=False):
        """
        Create a log in text format

        Parameters
        ----------
        accessed_only : bool, optional
            If True, only include options that were accessed, by default False

        Returns
        -------
        list
            List of strings representing the log, including linebreaks.
        """
        log=[]
        log.append("cd "+os.getcwd())
        log.append("python3 "+" ".join(sys.argv))
        lines=self._to_string(accessed_only=accessed_only)
        lines=['#'+line for line in lines]
        log.extend(lines)
        return log
    

    def _create_log_dict(self, accessed_only=False):
        """Create a log dictionary.

        Example:
        {
            "dependencies": {"log1.log"{...}, "log2.log": {...}}
            "date": "2020-01-01 12:00:00",
            "program": "Program1.py",
            "version": "1.0.0",
            "input": "Config1.ini",
            "runtime": "0:00:00",
            "options": {
                "DEFAULT": {},
                "Sec1": {
                    "user": 1.0
                }
            },
            "output_files": [
                {
                    "path": "output.txt",
                    "hash": "1234567890abcdef"
                }
            ]
        }
        Parameters
        ----------
        accessed_only : bool, optional
            If True, only include parameters that were accessed, by default False
        Returns:
            dict -- dictionary with the log information.
        """
        log={}
        log["date"]=str(datetime.datetime.now())
        log["program"]=self._get_program_file()
        log["arguments"]=sys.argv[1:]
        log["version"]=self.version
        log["input"]=str(self.filename)
        log["runtime"]=str(datetime.datetime.now()-self.creation_date)
        if accessed_only:
            log["options"]=self.get_accessed_options()
        else:
            log["options"]=self.options.to_leafdict()
        log["output_files"]=[{"path": str(path), "hash": self.hash_file(path)} for path in self.outfilenames]
        return log

    def show_data(self):
        """Print log."""
        print(*self._to_string(accessed_only=False))
    
    def __str__(self):
        """Get log as string."""
        return "".join(self._to_string(accessed_only=False))
    
    def __repr__(self):
        return "".join(self._to_string(accessed_only=False))



    def _write_log_txt(self, new_logs, old_logs, accessed_only=False):
        old_lines=[]
        log=self._create_log_txt(accessed_only=accessed_only)
        for old in old_logs:
            with open(old, "r") as oldfile:
                old_lines.extend(oldfile.readlines())
                old_lines[-1]=old_lines[-1].strip("\n")+"\n"
                old_lines.extend(f"# <Logfile> {old}\n") #This has to happen at the old logs! This way, even manually created logfiles get the path appended.
                old_lines.extend("#=========================================\n")
        for new in new_logs:
            with open(new, "w") as newfile:
                newfile.writelines(old_lines)
                newfile.writelines(log)
    
    def _write_log_json(self, new_logs: list, old_logs: list, accessed_only=False):
        dependencies={}
        for old in old_logs:
            try:
                with open(old, "r") as oldfile:
                    old_json=json.load(oldfile)
                    dependencies[str(old.resolve())]=old_json
            except json.decoder.JSONDecodeError:
                with open(old, "r") as oldfile:
                    dependencies[str(old.resolve())]={"text":oldfile.readlines()}
        log_json={}
        log_json.update(self._create_log_dict(accessed_only=accessed_only))
        log_json["dependencies"]=dependencies
        for new in new_logs:
            with open(new, "w") as newfile:
                json.dump(log_json, newfile, indent=4, default=str)

    @classmethod
    def _get_logfile_name(cls, file, file_ext, ext_modification_mode):
        if file is None:
            return []
        if isinstance(file, str) or isinstance(file, Path):
            file=[file]
        file=[Path(p) for p in file]
        if file_ext!=None:
            file_ext="."+file_ext.lstrip(".")
            if ext_modification_mode=='replace':
                file=[logfile.with_suffix(file_ext) for logfile in file]
            elif ext_modification_mode=='append':
                file=[logfile.with_suffix(logfile.suffix+file_ext) for logfile in file]
            else:
                raise ValueError(f"Unknown value for 'ext_modification_mode': {ext_modification_mode}")
        return file


    def write_log(self, new_logs, old_logs=None, file_ext='log', ext_modification_mode='append', format='json', accessed_only=True):
        """
        Write log to files.

        Read all old logfiles, combine with the log of the current program and save them to the new locations.

        Parameters
        ----------
        new_logs : str or Path or iterable of str, Path
            New logfiles to be created.
        old_logs : str or Path or iterable of str, Path, optional
            Existing logfiles, listed as dependencies in the new logfiles. (default: None)
        file_ext : str, optional
            If set, the file extensions of the provided paths are modified to 'file_ext' before the function is executed. (default: 'log')
        ext_modification_mode : str, optional
            How to modify the file extension. Can be 'replace' or 'append'. Only used if 'file_ext' is set. (default: 'append')
        format : str, optional
            Format of the new logfiles. Can be 'json' or 'txt'. (default: 'json')
        accessed_only : bool, optional
            If True, only the options that were accessed are written to the log. (default: True)
        """
        new_logs=self._get_logfile_name(new_logs, file_ext, ext_modification_mode)
        old_logs=self._get_logfile_name(old_logs, file_ext, ext_modification_mode)
        for i,f in enumerate(old_logs):
            if not f.exists():
                old_format=self._get_logfile_name(f.with_suffix(""), file_ext, 'replace')[0]
                if old_format.exists():
                    #Deprecation Warning
                    warnings.warn(f"Logfile {f} does not exist, but {old_format} was found. Will be using this instead. In inlog 2.2.0, the default behaviour changed from replacing file extensions to appending them. To get back the old behaviour, set ext_modification_mode='replace' in write_log().", DeprecationWarning)
                    old_logs[i]=old_format
                    
        if format=='json':
            self._write_log_json(new_logs, old_logs, accessed_only)
        elif format=='txt':
            self._write_log_txt(new_logs, old_logs, accessed_only)
        else:
            raise ValueError(f"Unknown format: {format}")




            
            




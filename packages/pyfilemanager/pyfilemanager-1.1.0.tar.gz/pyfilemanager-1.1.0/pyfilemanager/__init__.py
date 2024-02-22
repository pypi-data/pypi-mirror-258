"""Easy to use file search and file path management.

:py:class:`FileManager` class initializes file path management in the directory of interest.
:py:meth:`FileManager.add` is used to tag a set of file paths filtered based on different inclusion and exclusion criteria.
:py:meth:`FileManager.__getitem__` is used to retrieve file paths of interest based on a tag, filename, or pattern.
:py:func:`find` is the core function for finding files, and it is based on `os.walk` and `fnmatch`.
"""

from __future__ import annotations

import fnmatch
import os
from pathlib import Path
from typing import Callable, Iterable, Mapping, Union

__version__ = "1.1.0"
__all__ = ["FileManager", "find"]


class FileManager:
    """
    Easy to use file search and file path management.
    Add files using different inclusion and exclusion criteria under a 'tag'.
    Provides dictionary-like access to file-paths where the tags serve as keys.
    Useful for managing files in not-so-obviously organized folders.

    Args:
        base_dir (str): base directory for file search
        exclude_hidden (bool, optional): excludes hidden files when True. Defaults to True.

    Attributes:
        base_dir (str): base directory for file search

        _files (dict): {Tag: List of file paths}
        _filters (dict): {Tag: pattern list}
        _inclusions (dict): {Tag: inclusion criteria}
        _exclusions (dict): {Tag: exclusion criteria}

    IGNORE:
    Methods:
        add: Add files based on different inclusion and exclusion criteria.
        get_tags: Return a list of tags created using the add method.
        report: Print a report summarizing the size occupied by files under each tag.
        remove: Remove file paths stored under a given tag. May not be very useful.
        __getitem__: overloaded.

        _include, _exclude: Utilities used by the add method.
    IGNORE
    """

    def __init__(self, base_dir: str, exclude_hidden: bool = True):
        assert isinstance(base_dir, (str, Path))
        self.base_dir = os.path.realpath(base_dir)
        self._files = {}
        self._filters = {}
        self._inclusions = {}
        self._exclusions = {}
        assert isinstance(exclude_hidden, bool)
        self._exclude_hidden = exclude_hidden

    def add(
        self,
        tag: str = "all",
        pattern_list: Union[str, list[str]] = None,
        include: Union[str, list[str]] = None,
        exclude: Union[str, list[str]] = None,
        exclude_hidden: bool = None,
    ) -> FileManager:
        """Add files based on different inclusion and exclusion criteria.
        Call this method without any arguments to work with all the files in the directory using `FileManager.__getitem__`.
        Note that if a tag already exists, it will get overwritten with the new

        Examples:
            Add files that match the pattern *Camera*.avi under the tag `video`\n
            ``fm.add('video', '*Camera*.avi')``

            Add all files under the tag `all` (special case)\n
            ``fm = FileManager(r'C:\\videos').add()``

        Args:
            tag (str, optional): e.g. 'video_files'. Defaults to all, meaning add all files in the directory recursively.
            pattern_list (Union[str,list], optional): e.g. '*.avi', ['*.avi', '*.mp4']. Defaults to *.*
            include (Union[str,list], optional): Keep file paths that contain **all** of the supplied strings *anywhere* in the file path. Defaults to None.
            exclude (Union[str,list], optional): Disregard file paths that contain **any** of the supplied string anywhere in the file path. Defaults to None.
            exclude_hidden (bool, optional): Set the state for excluding hidden files. Defaults to the value of _exclude_hidden attribute, which defaults to True.

        Returns:
            FileManager: Returns self. Useful for chaining commands.
        """
        if pattern_list is None:
            assert tag == "all" or tag.startswith("*.")
            if tag == "all":
                pattern_list = "*.*"
            elif tag == "*.*":
                pattern_list = tag
                tag = "all"
            else:
                pattern_list = tag
                tag = tag[2:]
                assert not self._has_special_characters(tag)

        if isinstance(pattern_list, str):
            pattern_list = [pattern_list]

        if include is None:
            include = []
        if isinstance(include, str):
            include = [include]
        assert isinstance(include, (list, tuple))

        if exclude is None:
            exclude = []
        if isinstance(exclude, str):
            exclude = [exclude]
        assert isinstance(exclude, (list, tuple))

        if exclude_hidden is None:
            # None means not specified. In this case, set it to the global default.
            exclude_hidden = self._exclude_hidden

        self._files[tag] = []

        for pattern in pattern_list:
            self._files[tag] += find(
                pattern, path=self.base_dir, exclude_hidden=exclude_hidden
            )

        self._filters[tag] = pattern_list
        self._inclusions[tag] = []
        self._exclusions[tag] = []

        for inc_str in include:
            assert isinstance(inc_str, str)
            self._include(tag, inc_str)

        for exc_str in exclude:
            assert isinstance(exc_str, str)
            self._exclude(tag, exc_str)

        return self  # for chaining commands

    def add_by_depth(
        self,
        max_depth: int = 0,
        exclude_hidden: bool = None,
        include_directories: bool = False,
    ):
        """Add files and directories by their depth.
        Tags of name files0, and directories0 will be created for files and directories at depth0.

        Args:
            max_depth (int, optional): Maximum depth for the search. Defaults to 0, adding the top level contents only.
            exclude_hidden (bool, optional): Include or exclude hidden files and directories.
                Defaults to the value of self._exclude_hidden, which defaults to True.
            include_directories (bool, optional): When set to true, one tag will be created for directories, and one for files at each depth.
                When set to False, only the files tag will be created at each depth. Defaults to False.
        """
        if exclude_hidden is None:
            exclude_hidden = self._exclude_hidden

        directories, files = find_by_depth(
            path=self.base_dir, max_depth=max_depth, exclude_hidden=exclude_hidden
        )

        if include_directories:
            tag_items = dict(directories=directories, files=files)
        else:
            tag_items = dict(files=files)

        for item_name, item in tag_items.items():
            for depth, item_list in item.items():
                tag = f"{item_name}{depth}"
                self._files[tag] = item_list
                self._filters[tag] = []
                self._inclusions[tag] = []
                self._exclusions[tag] = []

        return self  # for chaining commands

    def remove(self, tag: str) -> None:
        """Remove file paths stored under the given tag.

        Args:
            tag (str): A tag created when using the add method.

        Raises:
            ValueError: If an unknown tag is supplied.
        """
        if tag in self._files:
            del self._files[tag]
        else:
            raise ValueError(f"Unknown type {tag}")

    def _include(self, tag: str, inclusion_string: str) -> None:
        """Include a set of files from the list. Useful for choosing files in specific sub-folders.
        Use this functionality using the add method.

        Args:
            tag (str): A tag created when using the add method.
            inclusion_string (str): File paths containing this string anywhere in the path will be kept.
        """
        assert tag in self._files
        self._files[tag] = [fn for fn in self._files[tag] if inclusion_string in fn]
        self._inclusions[tag].append(inclusion_string)

    def _exclude(self, tag: str, exclusion_string: str):
        """Exclude a set of files from the list. Useful for ignoring files in specific sub-folders.
        Use this functionality using the add method.

        Args:
            tag (str): A tag created when using the add method.
            exclusion_string (str): File paths containing this string anywhere in the path will be removed.
        """
        assert tag in self._files
        self._files[tag] = [fn for fn in self._files[tag] if exclusion_string not in fn]
        self._exclusions[tag].append(exclusion_string)

    def __getitem__(self, key: str) -> list:
        """Retrieve file paths based on -

            (0) `FileManager.filter` method if key has special chacters such as *, ?, !, []
            (1) tag
            (2) exact match for the 'stem' of the file
            (3) key is anywhere in the path

            Try (0) if there are special characters in `key`.
            If not, try (2) only if (1) doesn't return any results,
            and try (3) only if (2) doesn't return any results.

        Args:
            key (str): Either a tag, filename, or partial match.

        Returns:
            list: List of file paths.
        """
        # (0) filter using fnmatch.filter when there are special characters in the key
        if self._has_special_characters(key):
            # prepend a * to the key because the intention is to act on full file paths
            return self.filter(
                f"*{key}"
            )  # notes*.txt will return notes1.txt and notes2.txt

        # (1) by tag
        if key in self._files:
            return self._files[key]

        # (2) full-stem search
        all_files = self.all_files
        stem_to_path = {
            Path(x).stem: [] for x in all_files
        }  # in case there are multiiple files with the same 'stem'
        for file_name in all_files:
            stem_to_path[Path(file_name).stem].append(file_name)
        if key in stem_to_path:
            return stem_to_path[key]

        # (3) loose search - full path contains
        return self._unique_sorted([x for x in all_files if key in x])

    def filter(self, pattern: str) -> list:
        """Filter self.all_files using `fnmatch.filter`.

        Args:
            pattern (str): e.g. *.avi, *notes?.txt

        Returns:
            list: List of file paths.
        """
        return fnmatch.filter(self.all_files, pattern)

    def get_tags(self) -> list:
        """Return a list of tags created using the add method.

        Returns:
            list: List of tags.
        """
        return list(self._files.keys())

    @property
    def all_files(self) -> list:
        """Return a list of all files managed by the filemanager. Remove duplicates.

        Returns:
            list: List of file paths
        """
        ret = []
        for ftype in self.get_tags():
            ret += self[ftype]
        return self._unique_sorted(ret)

    def report(self, units: str = "MB") -> None:
        """Print a report summarizing the size occupied by files under each tag.

        Args:
            units (str, optional): One of ('B', 'KB', 'MB', 'GB', 'TB). B is for bytes. Defaults to 'MB'.
        """
        for file_type, file_list in self._files.items():
            fs = sum(list(get_file_sizes(file_list, units=units).values()))
            print(
                str(len(file_list))
                + " "
                + file_type
                + " files taking up {:4.3f} ".format(fs)
                + units
            )

    @staticmethod
    def _unique_sorted(file_list: list) -> list:
        """Utility to return a sorted list of unique items in the input list.

        Args:
            file_list (list): Expected to be a list of strings (file names).

        Returns:
            list: List of unique elements (file names).
        """
        ret = list(set(file_list))
        ret.sort()
        return ret

    @staticmethod
    def _has_special_characters(
        inp: str, spc: Iterable[str] = ("*", "?", "[", "!")
    ) -> bool:
        """Helper function to deal with special use-cases of `FileManager.add` and `FileManager.__getitem__` methods.

        Args:
            inp (str): e.g. *notes, avi
            spc (Iterable[str], optional): Described in `fnmatch.fnmatch`. Defaults to ('*', '?', '[', '!').

        Returns:
            bool: True if any of the special characters are in `inp`
        """
        return any([s in inp for s in spc])


def find(pattern: str, path: str = None, exclude_hidden: bool = True) -> list:
    """Core function for finding files based on ``os.walk`` and ``fnmatch``.

    Example:
        ``find('*.txt', r'C:\\videos')``

    Args:
        pattern (str): Input for fnmatch.
        path (str, optional): Search for files in this path. Defaults to the results of os.getcwd().
        exclude_hidden (bool, optional): Whether to include filenames of hidden files. Defaults to True.

    Returns:
        list: List of file names.
    """
    if path is None:
        path = os.getcwd()

    _eh = _get_exclude_hidden_func(exclude_hidden)

    result = []
    for root, dirs, files in os.walk(path):
        result += [
            os.path.join(root, name) for name in fnmatch.filter(_eh(files), pattern)
        ]
        dirs[:] = _eh(dirs)

    return result


def find_by_depth(
    path: str, max_depth: int = 0, exclude_hidden: bool = True
) -> tuple[Mapping[int, list[str]], Mapping[int, list[str]]]:
    """Get full paths to directories and files in path, organized by their depth.
    Convenient to retrieve files in the current path without looking in the sub-directories.

    Args:
        path (str): Search for files and directories in this path.
        max_depth (int, optional): Maximum depth for the search. Set this to -1 to search everything.
            But if that is the case, simply use FileManager.add without any arguments. Defaults to 0.
        exclude_hidden (bool, optional): When true, exclude hidden files and folders from the serach. Defaults to True.

    Returns:
        tuple[Mapping[int, list[str]], Mapping[int, list[str]]]: _description_
    """
    ret_dirs, ret_files = {}, {}

    _eh = _get_exclude_hidden_func(exclude_hidden)

    def _dirs_files_in_path(this_path):
        _, dirs, files = next(os.walk(this_path))
        dirs = [os.path.join(this_path, dir) for dir in _eh(dirs)]
        files = [os.path.join(this_path, file) for file in _eh(files)]
        return dirs, files

    ret_dirs[0], ret_files[0] = _dirs_files_in_path(path)

    if max_depth == -1:
        cond_func = lambda _: True
    else:
        cond_func = lambda cl: cl <= max_depth

    current_level = 1
    while cond_func(current_level):
        if not ret_dirs[current_level - 1]:
            break

        ret_dirs[current_level], ret_files[current_level] = [], []

        for path in ret_dirs[current_level - 1]:
            dirs, files = _dirs_files_in_path(path)
            ret_dirs[current_level] += dirs
            ret_files[current_level] += files

        current_level += 1

    return ret_dirs, ret_files


def get_file_sizes(file_list: list, units: str = "MB") -> dict:
    """Returns files sizes in descending order (default: megabytes). Used by the FileManager.report method.

    Args:
        file_list (list): list of file names
        units (str, optional): One of ('B', 'KB', 'MB', 'GB', 'TB). B is for bytes. Defaults to 'MB'.

    Returns:
        dict: {file_name : size}
    """
    div = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
    if isinstance(file_list, str):
        file_list = [file_list]
    assert isinstance(file_list, list)
    size_mb = {
        os.path.getsize(f) / div[units]: f for f in file_list
    }  # {size: file_name}
    size_list = list(size_mb.keys())
    size_list.sort(reverse=True)
    return {size_mb[s]: s for s in size_list}  # {file_name : size}


def _exclude_hidden(name_list: list[str]) -> list[str]:
    """Exclude names of hidden files / folders

    Args:
        name_list (list): list of strings containing just the names of the files or folder (without the path).

    Returns:
        list: List of names that don't start with ~$, ., or if the name is #recycle
    """
    return [
        name
        for name in name_list
        if not any([name.startswith("~$"), name.startswith("."), name == "#recycle"])
    ]


def _get_exclude_hidden_func(exclude_hidden: bool = True) -> Callable:
    """Return a function that processes a list of names based on whether hidden names should be included or excluded.

    Args:
        exclude_hidden (bool, optional): If True, return a function that excludes hidden names.
            Else, return a function that simply returns its input list. Defaults to True.

    Returns:
        Callable: A function that takes a list of strings, and returns a list of strings.
            This function will exclude hidden files/directories if exclude_hidden is set to True.
    """
    if exclude_hidden:
        return _exclude_hidden
    return lambda x: x

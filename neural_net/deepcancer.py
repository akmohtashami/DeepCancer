class Network(object):
    def __init__(self):
        # Load network here
        import time
        time.sleep(10)

    def run(self, dir):
        """
        The dir is a directory containing the input file (named "input").
        You are only allowed to read from / write to this directory
        (you may invoke scripts from other parts of system)
        When finished, you must return a list representing the output files.
        each element of a list is either a 2-tuple (name, path)
        or a 4-tuple(name, path, link, include).
        in the latter case, link and includes are two booleans determining
        whether there should be a link to download the file in
        the results page and whether the contents of the file should be
        pasted into the results page(e.g. an html diagram), respectively.

        Example:
            return [("woohoo", os.path.join(dir, "output")),
                ("woohoo2", os.path.join(dir, "output"), True, False),
                ("woohoo3", os.path.join(dir, "output"), False, True)]
        """
        import shutil
        import os
        shutil.copy(os.path.join(dir,"input"),
                    os.path.join(dir, "output"),)
        return [("woohoo", os.path.join(dir, "output")),
                ("woohoo2", os.path.join(dir, "output"), True, False),
                ("woohoo3", os.path.join(dir, "output"), False, True)]
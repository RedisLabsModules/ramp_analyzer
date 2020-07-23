import cmd
import os
import zipfile
import json
import StringIO
import sys
import inquirer

class Colors(object):
    @staticmethod
    def Cyan(data):
        return '\033[36m' + data + '\033[0m'

    @staticmethod
    def Yellow(data):
        return '\033[33m' + data + '\033[0m'

    @staticmethod
    def Bold(data):
        return '\033[1m' + data + '\033[0m'

    @staticmethod
    def Bred(data):
        return '\033[31;1m' + data + '\033[0m'

    @staticmethod
    def Gray(data):
        return '\033[30;1m' + data + '\033[0m'

    @staticmethod
    def Lgray(data):
        return '\033[30;47m' + data + '\033[0m'

    @staticmethod
    def Blue(data):
        return '\033[34m' + data + '\033[0m'

    @staticmethod
    def Green(data):
        return '\033[32m' + data + '\033[0m'

class RampAnalizer(cmd.Cmd):
    def __init__(self, filePath):
        cmd.Cmd.__init__(self)
        self.zf = None
        self.jsonObj = None
        self.prompt = Colors.Green('ramp-Analizer > ')
        self.do_EOF = self.do_exit
        help_EOF = self.help_exit
        self._reset()
        if filePath:
            self.do_open(filePath)

    def _reset(self):
        if self.zf is not None:
            self.zf.close()
        self.zf = None
        self.jsonObj = None
        self.prompt = Colors.Green('ramp-Analizer > ')

    def do_save(self, line):
        '''
        Save the ramp file to disc
        '''
        if self.zf is None:
            print(Colors.Bred('No file is open'))
            return False

        strio = StringIO.StringIO()
        with zipfile.ZipFile(strio, "a", zipfile.ZIP_DEFLATED, False) as newZip:
            for f in self.zf.filelist:
                if f.filename == 'module.json':
                    data = json.dumps(self.jsonObj, indent=2)
                else:
                    data = self.zf.read(f.filename)
                newZip.writestr(f.filename, data)

        filePath = self.zf.filename
        self.zf.close()
        with open(filePath, 'wb') as f:
            strio.seek(0)
            f.write(strio.read())

        print(Colors.Green('Saved %s' % filePath))

        self._reset()
        self.do_open(filePath)


    def do_dumpjson(self, line):
        '''
        Dump the entire module.json file
        '''
        if self.zf is None:
            print(Colors.Bred('No file is open'))
            return False

        print(json.dumps(self.jsonObj, indent=2))

    def do_dumpfiles(self, line):
        '''
        Dump all the files in the ramp.zip
        '''
        if self.zf is None:
            print(Colors.Bred('No file is open'))
            return False

        for f in self.zf.filelist:
            print(Colors.Cyan(f.filename))

    def do_dumpdeps(self, line):
        '''
        Dump the dependencies and optional-dependencies section in the ramp file
        '''
        if self.zf is None:
            print(Colors.Bred('No file is open'))
            return False

        print(Colors.Bold('dependencies:'))
        deps = self.jsonObj['dependencies']
        print(Colors.Cyan(json.dumps(deps, indent=2)))
        print('')
        print(Colors.Bold('optional-dependencies:'))
        deps = self.jsonObj['optional-dependencies']
        print(Colors.Cyan(json.dumps(deps, indent=2)))

    def do_rewritedeps(self, line):
        '''
        Rewrite the dependencies section of the ramp.
        '''
        if self.zf is None:
            print(Colors.Bred('No file is open'))
            return False

        currSelected = set(self.jsonObj['dependencies'].keys())
        depsList = set(self.jsonObj['dependencies'].keys() + self.jsonObj['optional-dependencies'].keys())

        questions = [inquirer.Checkbox(
                        'deps',
                        message="Choose dependencies",
                        choices=depsList,
                        default=currSelected,
                        )
                    ]
        answers = inquirer.prompt(questions)  # returns a dict

        deps = answers['deps']
        newDeps = {}
        currDeps = self.jsonObj['dependencies']
        currOptionalDeps = self.jsonObj['optional-dependencies']
        for dep in deps:
            if dep in currDeps.keys():
                newDeps[dep] = currDeps[dep]
                continue
            if dep in currOptionalDeps.keys():
                newDeps[dep] = currOptionalDeps[dep]
                continue
            print(Colors.Bred('Dependency %s not found' % dep))
            return False
        self.jsonObj['dependencies'] = newDeps
        print(Colors.Green('Dependencies changed'))

        questions = [
        inquirer.List('save',
                message="Save?",
                choices=['YES', 'NO'],
            ),
        ]
        answers = inquirer.prompt(questions)

        if answers['save'] == 'YES':
            self.do_save('')

    def do_open(self, line):
        '''
        Open a ramp file to work on
        '''
        if self.zf is not None:
            print(Colors.Bred('Another file is already open, close it first!!!'))
            return False

        if not os.path.exists(line):
            print(Colors.Bred('No such fule'))
            return False
        try:
            self.zf = zipfile.ZipFile(line, "r", zipfile.ZIP_DEFLATED, False)
        except Exception as e:
            print(Colors.Bred('Failed open zip file, %s' % str(e)))
            return False
        jsonFile = [a for a in self.zf.filelist if a.filename == 'module.json']
        if len(jsonFile) != 1:
            print(Colors.Bred('Invalid ramp format'))
            self.zf = None
            return False
        try:
            self.jsonObj = json.loads(self.zf.read(jsonFile[0].filename))
        except Exception as e:
            print(Colors.Bred('Failed read ramp json file, %s' % str(e)))
            self.zf = None
            return False
        self.prompt = Colors.Green('ramp-modifier %s > ' % self.zf.filename)

    def do_close(self, line):
        '''
        Close the current open file
        '''
        if self.zf is None:
            print(Colors.Bred('No file is open'))
            return False
        self._reset()

    def do_exit(self, line):
        print(Colors.Green('BYE BYE'))
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

def main():
    filePath = None

    if len(sys.argv) > 1:
        filePath = sys.argv[1]

    cmd = RampAnalizer(filePath)
    cmd.cmdloop()
    

if __name__ == '__main__':
    main()
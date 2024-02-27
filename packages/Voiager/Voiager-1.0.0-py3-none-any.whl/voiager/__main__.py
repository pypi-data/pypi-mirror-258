import sys
import yaml
from voiager import Voiager
from voiager import launch


def main():
    parser = Voiager.parseParamsFile()
    args = parser.parse_args()
    file = args.parameters
    params = yaml.safe_load(file)
    vger = Voiager(params)
    if not vger.runExec:
        sys.exit('Voiager has been installed successfully! Set \'runExec=True\' in \'params.yaml\' to run it.')
    else:
        print('Launching Voiager...')
        launch(vger)

if __name__ == '__main__':
    main()
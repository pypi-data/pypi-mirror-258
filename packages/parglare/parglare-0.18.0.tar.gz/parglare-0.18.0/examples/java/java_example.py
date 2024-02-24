import os
import time

from parglare import GLRParser, Grammar


def main(debug=False):
    this_folder = os.path.dirname(__file__)

    g = Grammar.from_file(os.path.join(this_folder, 'java16.pg'))
    parser = GLRParser(g, debug=debug, debug_colors=True)

    file_name = os.path.join(this_folder, 'TomcatServletWebServerFactory.java')
    file_size = os.path.getsize(file_name)

    t_start = time.time()
    forest = parser.parse_file(file_name)
    t_end = time.time()

    print(f'Elapsed time: {t_end - t_start:.2f}', 'sec')
    print(f'Speed = {file_size/1000/(t_end - t_start):.2f}',
          'KB/sec\n')
    print('Solutions: ', forest.solutions)
    print('Ambiguities: ', forest.ambiguities)


if __name__ == "__main__":
    main(debug=False)

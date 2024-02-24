import argparse
from jnb.filegen import FileGen
from jnb.nbmeta import NBMeta
from jnb.parsedata import ParseData


def main():
    args = ParseData.parse_data()

    # for filename in args.create:
    #     FileGen.create_file(
    #         filename,
    #         NBMeta.get_notebook_content(),
    #     )
    FileGen.create_files(args.create, NBMeta.get_notebook_content())


if __name__ == "__main__":
    main()

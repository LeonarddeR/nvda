# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import argparse
import io
import json
import os
from typing import DefaultDict, Iterable, NamedTuple, TYPE_CHECKING

import globalVars
import languageHandler

if TYPE_CHECKING:
	import brailleTables


def encodeNamedTuple(nt: NamedTuple):
	return {
		key: value
		for key, value in nt._asdict().items()
		if key not in nt._field_defaults or value != nt._field_defaults[key]
	}


def createAddTableStatement(table: "brailleTables.BrailleTable") -> str:
	dct = encodeNamedTuple(table)
	writer = io.StringIO()
	writer.writelines(
		[
			"# Translators: The name of a braille table displayed in the",
			"# braille settings dialog.",
		],
	)
	writer.write(f"""addTable({dct['fileName']!r}, {dct['displayName']!r}, """)


def _writeToJson(data: Iterable, outputFile: str) -> None:
	with open(outputFile, "w", encoding="utf-8") as f:
		json.dump(data, f, indent="\t")


def generateBuiltInTablesJson(outputFile: str) -> None:
	import brailleTables

	inputTableForLangs = DefaultDict(list)
	for lang, tableFileName in brailleTables._inputTableForLangs.items():
		inputTableForLangs[tableFileName].append(lang)
	outputTableForLangs = DefaultDict(list)
	for lang, tableFileName in brailleTables._outputTableForLangs.items():
		outputTableForLangs[tableFileName].append(lang)
	data = []
	for fileName, table in brailleTables._tables.items():
		dct = encodeNamedTuple(table)
		if langs := inputTableForLangs.get(fileName):
			dct["inputForLangs"] = langs
		if langs := outputTableForLangs.get(fileName):
			dct["outputForLangs"] = langs

		data.append(dct)
	_writeToJson(data, outputFile)


def generateLiblouisTablesJson(outputFile: str) -> None:
	import brailleTables

	os.environ["LOUIS_TABLEPATH"] = brailleTables.TABLES_DIR
	with os.add_dll_directory(globalVars.appDir):
		import louis

	louisTables = sorted(louis.listTables())
	nvdaTables = []
	for table in louisTables:
		fileName = os.path.basename(table)
		dct = {
			"fileName": fileName,
			"displayName": louis.getTableInfo(fileName, "display-name"),
		}
		if louis.getTableInfo(fileName, "contraction") in ("partial", "full"):
			dct["contracted"] = True
		nvdaTables.append(dct)

	_writeToJson(nvdaTables, outputFile)


def generateTablesModule(inputFile: str, outputFile: str) -> None:
	with open(inputFile, "r", encoding="utf-8") as input:
		tables = json.load(input)


def main():
	globalVars.appDir = os.path.join(os.path.dirname(__file__), "source")
	languageHandler.setLanguage("en")
	args = argparse.ArgumentParser()
	commands = args.add_subparsers(title="commands", dest="command", required=True)
	command_generateBuiltInJson = commands.add_parser(
		"builtIn",
		help="Generate a JSON document from the current list of built-in tables.",
	)
	command_generateBuiltInJson.add_argument(
		"outputFile",
		help="The path to the JSON file to output",
	)
	command_generateLiblouisJson = commands.add_parser(
		"liblouis",
		help="Generate a JSON document from liblouis metadata.",
	)
	command_generateLiblouisJson.add_argument(
		"outputFile",
		help="The path to the JSON file to output",
	)

	args = args.parse_args()
	match args.command:
		case "builtIn":
			generateBuiltInTablesJson(outputFile=args.outputFile)
		case "liblouis":
			generateLiblouisTablesJson(outputFile=args.outputFile)
		case _:
			raise ValueError(f"Unknown command {args.command}")


if __name__ == "__main__":
	main()

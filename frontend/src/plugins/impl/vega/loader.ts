/* Copyright 2024 Marimo. All rights reserved. */
// @ts-expect-error - no types
import { loader as createLoader, read, typeParsers } from "vega-loader";
import { DataFormat } from "./types";

// Augment the typeParsers to support Date
typeParsers.date = (value: string) => new Date(value).toISOString();

export const vegaLoader = createLoader();

/**
 * Load data from a URL and parse it according to the given format.
 *
 * This resolves to an array of objects, where each object represents a row.
 */
export function vegaLoadData(
  url: string,
  format: DataFormat | undefined | { type: "csv"; parse: "auto" },
): Promise<object[]> {
  return vegaLoader.load(url).then((csvData: string) => {
    // CSV data comes columnar and may have duplicate column names.
    // We need to uniquify the column names before parsing since vega-loader
    // returns an array of objects which drops duplicate keys.
    //
    // We make the column names unique by appending a number to the end of
    // each duplicate column name. If we want to preserve the original key
    // we would need to store the data in columnar format.
    csvData = uniquifyColumnNames(csvData);

    // csv -> json
    return read(csvData, format);
  });
}

export function uniquifyColumnNames(csvData: string): string {
  if (!csvData || !csvData.includes(",")) {
    return csvData;
  }

  const lines = csvData.split("\n");
  const header = lines[0];
  const headerNames = header.split(",");

  const existingNames = new Set<string>();
  const newNames = [];
  for (const name of headerNames) {
    const uniqueName = getUniqueKey(name, existingNames);
    newNames.push(uniqueName);
    existingNames.add(uniqueName);
  }

  const uniqueHeader = newNames.join(",");
  lines[0] = uniqueHeader;
  return lines.join("\n");
}

export const ZERO_WIDTH_SPACE = "\u200B";

function getUniqueKey(key: string, existingKeys: Set<string>): string {
  let result = key;
  let count = 1;
  while (existingKeys.has(result)) {
    result = `${key}${ZERO_WIDTH_SPACE.repeat(count)}`;
    count++;
  }

  return result;
}

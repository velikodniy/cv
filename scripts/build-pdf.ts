import { parse as parseYaml } from "@std/yaml";
import { ensureDir } from "@std/fs";
import { join } from "node:path";

const YAML_FILE = "data.yaml";
const OUTPUT_DIR = "public";

async function buildPdf() {
  const yamlContent = await Deno.readTextFile(YAML_FILE);
  const data = parseYaml(yamlContent) as { pdf_filename: string };

  if (!data.pdf_filename) {
    throw new Error(`"pdf_filename" field not found in ${YAML_FILE}`);
  }

  const outputPath = join(OUTPUT_DIR, data.pdf_filename);

  await ensureDir(OUTPUT_DIR);

  const command = new Deno.Command("typst", {
    args: [
      "compile",
      "--root",
      ".",
      "typst/cv.typ",
      "--font-path",
      "typst/fonts/",
      outputPath,
    ],
    stdout: "inherit",
    stderr: "inherit",
  });

  const { code } = await command.output();

  if (code !== 0) {
    console.error("Typst compilation failed");
    Deno.exit(code);
  }

  console.log(`Generated PDF: ${outputPath}`);
}

if (import.meta.main) {
  buildPdf();
}

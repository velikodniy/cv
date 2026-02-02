import { parseArgs } from "jsr:@std/cli/parse-args";
import sharp from "npm:sharp";
import { join } from "node:path";
import { ensureDir, copy } from "jsr:@std/fs";
import { parse as parseYaml } from "jsr:@std/yaml";

const FAVICON_SPECS = [
  { size: 16, name: "favicon-16x16.png" },
  { size: 32, name: "favicon-32x32.png" },
  { size: 180, name: "apple-touch-icon.png" },
  { size: 192, name: "android-chrome-192x192.png" },
  { size: 512, name: "android-chrome-512x512.png" },
];

const ICO_SIZES = [16, 32];

async function generateFavicons(
  yamlPath: string,
  outputDir: string,
  enhance: boolean = true
) {
  await ensureDir(outputDir);

  const yamlContent = await Deno.readTextFile(yamlPath);
  const data = parseYaml(yamlContent) as { photo: string };

  if (!data.photo) {
    throw new Error(`"photo" field not found in ${yamlPath}`);
  }

  const inputPath = data.photo;

  console.log(`Processing image: ${inputPath}`);

  const image = sharp(inputPath);
  const metadata = await image.metadata();

  if (!metadata.width || !metadata.height) {
    throw new Error("Could not get image metadata");
  }

  // Crop to square
  const size = Math.min(metadata.width, metadata.height);
  const pipeline = image
    .extract({
      left: Math.floor((metadata.width - size) / 2),
      top: Math.floor((metadata.height - size) / 2),
      width: size,
      height: size,
    })
    .resize(size, size);

  // Enhance if requested
  if (enhance) {
    pipeline.modulate({
      brightness: 1.0,
      saturation: 1.0,
    }).sharpen({
      sigma: 1.0,
      m1: 1.0,
      m2: 0,
      x1: 2,
      y2: 10,
      y3: 20,
    });
  }

  const buffer = await pipeline.toBuffer();

  // Generate PNGs
  for (const spec of FAVICON_SPECS) {
    let resized = sharp(buffer).resize(spec.size, spec.size, {
      kernel: sharp.kernel.lanczos3,
    });

    if (enhance) {
       resized = resized.linear(1.1, -(128 * 1.1) + 128);
    }

    if (spec.size <= 32) {
      resized = resized.sharpen({
        sigma: 0.5,
        m1: 0.5,
      });
    }

    await resized.toFile(join(outputDir, spec.name));
    console.log(`Generated ${spec.name}`);
  }

  // Generate ICO
  const icoBuffers = [];
  for (const size of ICO_SIZES) {
    const resized = sharp(buffer).resize(size, size, {
      kernel: sharp.kernel.lanczos3,
    });

    if (size <= 32) {
       resized.sharpen({ sigma: 0.5 });
    }

    icoBuffers.push(await resized.png().toBuffer());
  }

  await writeIco(join(outputDir, "favicon.ico"), icoBuffers);
  console.log("Generated favicon.ico");

  const destPath = join(outputDir, data.photo);
  await copy(inputPath, destPath, { overwrite: true });
  console.log(`Copied ${inputPath} to ${destPath}`);
}

async function writeIco(path: string, pngBuffers: Uint8Array[]) {
  const count = pngBuffers.length;
  const headerLen = 6;
  const directoryLen = 16 * count;
  let offset = headerLen + directoryLen;

  const header = new Uint8Array(6);
  const view = new DataView(header.buffer);
  view.setUint16(0, 0, true); // Reserved
  view.setUint16(2, 1, true); // Type (1=ICO)
  view.setUint16(4, count, true); // Count

  const directories = [];
  const validBuffers = [];

  for (const png of pngBuffers) {
    const img = sharp(png);
    const meta = await img.metadata();
    const width = meta.width!;
    const height = meta.height!;
    const size = png.length;

    const dir = new Uint8Array(16);
    const dirView = new DataView(dir.buffer);
    dirView.setUint8(0, width >= 256 ? 0 : width);
    dirView.setUint8(1, height >= 256 ? 0 : height);
    dirView.setUint8(2, 0); // Palette count
    dirView.setUint8(3, 0); // Reserved
    dirView.setUint16(4, 1, true); // Color planes
    dirView.setUint16(6, 32, true); // Bits per pixel
    dirView.setUint32(8, size, true); // Size
    dirView.setUint32(12, offset, true); // Offset

    directories.push(dir);
    validBuffers.push(png);
    offset += size;
  }

  const file = await Deno.open(path, { write: true, create: true, truncate: true });
  await file.write(header);
  for (const dir of directories) await file.write(dir);
  for (const buf of validBuffers) await file.write(buf);
  file.close();
}

async function main() {
  const args = parseArgs(Deno.args, {
    string: ["output-dir"],
    boolean: ["no-enhance"],
    alias: { o: "output-dir" },
    default: { "output-dir": "." },
  });

  if (args._.length < 1) {
    console.error("Usage: generate-favicons.ts <data.yaml> [options]");
    Deno.exit(1);
  }

  const yamlFile = String(args._[0]);
  const output = args["output-dir"];
  const enhance = !args["no-enhance"];

  try {
    await generateFavicons(yamlFile, output, enhance);
  } catch (error) {
    console.error("Error:", error);
    Deno.exit(1);
  }
}

if (import.meta.main) {
  main();
}

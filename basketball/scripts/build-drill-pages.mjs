import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sourceHtml = await readFile(path.join(projectRoot, "index.html"), "utf8");
const drillDirectory = path.join(projectRoot, "data", "drills");
const drillFiles = (await readdir(drillDirectory)).filter((file) => file.endsWith(".js")).sort();

for (const file of drillFiles) {
  const source = await readFile(path.join(drillDirectory, file), "utf8");
  const id = source.match(/\bid:\s*"([^"]+)"/)?.[1];
  const title = source.match(/\btitle:\s*"([^"]+)"/)?.[1];
  const status = source.match(/\bstatus:\s*"([^"]+)"/)?.[1];
  if (!id || !title || status !== "ready") continue;

  const pageDirectory = path.join(projectRoot, "drills", id);
  const pageHtml = sourceHtml
    .replace("<head>", '<head>\n    <base href="../../">')
    .replace("<title>Basketball Drills</title>", `<title>${title} | Basketball Drills</title>`);

  await mkdir(pageDirectory, { recursive: true });
  await writeFile(path.join(pageDirectory, "index.html"), pageHtml);
  console.log(`/drills/${id}/`);
}

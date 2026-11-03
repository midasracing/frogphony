# Frogphony
React + TypeScript + Vite. Polish music education frontend with Kumka, the pink toad.

## Development
Node 22.13+: `npm install`, `npm run dev`. Production: `npm run build`.

## GitHub Pages
In repository Settings → Pages, choose **GitHub Actions** as the source.
Pushes to `main` build and deploy via `.github/workflows/pages.yml`.
Expected address after successful deployment: https://midasracing.github.io/frogphony/
Vite base is `/frogphony/`; change it if the repository is renamed or a custom domain is added.

Three demo lessons, local progress, responsive UI. Synthetic audio preview; verified piano samples and Rive animation are not implemented yet. Progress is per origin and does not transfer automatically from the previous preview.

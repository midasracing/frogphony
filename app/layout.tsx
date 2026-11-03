import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = {title:'Frogphony — złap swój rytm',description:'Twoja muzyczna podróż. Kształcenie słuchu, teoria i nauka o muzyce z Kumką.'};
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>){return <html lang="pl"><body>{children}</body></html>}

"use client";

import "./globals.css";
import { EmailProvider } from "../context/EmailContext";


export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <EmailProvider>
          {children}
        </EmailProvider>
      </body>
    </html>
  );
}

"use client";

import "./globals.css";
import { EmailProvider } from "../context/EmailContext";
import { GoogleOAuthProvider } from "@react-oauth/google";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <GoogleOAuthProvider clientId="108739963658-cnrpov3phjgq2k5mc0ajvn20u917jgnd.apps.googleusercontent.com">
          <EmailProvider>
            {children}
          </EmailProvider>
        </GoogleOAuthProvider>
      </body>
    </html>
  );
}

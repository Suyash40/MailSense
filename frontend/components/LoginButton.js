"use client";

import { useGoogleLogin } from "@react-oauth/google";

export default function LoginButton({ onLogin }) {

  const login = useGoogleLogin({
    scope: "https://www.googleapis.com/auth/gmail.readonly",
    onSuccess: async (tokenResponse) => {

      const res = await fetch("http://localhost:8000/auth/google", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          access_token: tokenResponse.access_token
        })
      });

      const data = await res.json();
      onLogin(data);
    }
  });

  return (
    <button
      onClick={() => login()}
      className="bg-green-500 text-black px-6 py-2 rounded font-bold"
    >
      Login with Google
    </button>
  );
}

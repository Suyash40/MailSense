"use client";

import LoginButton from "../../components/LoginButton";
import { useEmails } from "../../context/EmailContext";

export default function LoginPage() {

    const { login } = useEmails();

    return (
        <div className="min-h-screen bg-black text-green-400 flex flex-col items-center justify-center">

            <h1 className="text-3xl font-bold mb-6">MailSense AI</h1>

            <p className="mb-4 text-gray-400">
                Login to access your AI-powered inbox
            </p>

            <LoginButton
                onLogin={(userData) => {
                    localStorage.removeItem("user"); // clear old
                    login(userData);
                    window.location.replace("/");   // hard refresh
                }}
            />



        </div>
    );
}

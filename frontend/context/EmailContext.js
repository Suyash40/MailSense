"use client";

import { createContext, useContext, useEffect, useState } from "react";

const EmailContext = createContext();

export function EmailProvider({ children }) {

  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);

useEffect(() => {
  fetch("http://localhost:8000/emails")
    .then(res => res.json())
    .then(data => {
      console.log("EMAIL CONTEXT DATA 👉", data); // 👈 ADD THIS
      setEmails(data.emails || []);
      setLoading(false);
    })
    .catch(err => {
      console.error("FETCH ERROR ❌", err);
      setLoading(false);
    });
}, []);


  return (
    <EmailContext.Provider value={{ emails, loading }}>
      {children}
    </EmailContext.Provider>
  );
}

export function useEmails() {
  return useContext(EmailContext);
}

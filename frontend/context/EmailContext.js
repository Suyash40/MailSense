"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { useRef } from "react";

const EmailContext = createContext();

export function EmailProvider({ children }) {

  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [offset, setOffset] = useState(0);
  const fetchedOnce = useRef(false);

  const [user, setUser] = useState(
    typeof window !== "undefined"
      ? JSON.parse(localStorage.getItem("user"))
      : null
  );

  const LIMIT = 10;

  const fetchEmails = async (newOffset = 0, append = false) => {

    setLoading(true);

    try {
      const res = await fetch(
        `http://localhost:8000/emails?limit=${LIMIT}&offset=${newOffset}`
      );

      const data = await res.json();

      if (append) {
        setEmails(prev => [...prev, ...data.emails]);
      } else {
        setEmails(data.emails);
      }

      setOffset(newOffset + LIMIT);

    } catch (err) {
      console.error("FETCH FAILED:", err);
    }

    setLoading(false);
  };

useEffect(() => {
  if (!user) return;

  if (fetchedOnce.current) return;   // prevent double call
  fetchedOnce.current = true;

  fetchEmails(0, false);
}, [user]);



  const loadMore = () => {
    fetchEmails(offset, true);
  };

  const login = (userData) => {
    localStorage.setItem("user", JSON.stringify(userData));
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem("user");
    setUser(null);
    setEmails([]);
    setOffset(0);
  };

  return (
    <EmailContext.Provider value={{
      emails,
      loading,
      user,
      login,
      logout,
      loadMore
    }}>
      {children}
    </EmailContext.Provider>
  );
}

export function useEmails() {
  return useContext(EmailContext);
}

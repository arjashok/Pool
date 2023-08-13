import React, {useContext, useState, useEffect} from "react";
import { auth } from "../firebase";
import { createUserWithEmailAndPassword, User, onAuthStateChanged } from "firebase/auth";

type AuthContextType = {
    currentUser: User | null;
    signup: (email: string, password: string) => Promise<unknown>;
};

const AuthContext = React.createContext<AuthContextType>({
    currentUser: auth.currentUser,
    signup: (email: string, password: string) => createUserWithEmailAndPassword(auth, email, password),
});

export function useAuth() {
    return useContext(AuthContext);
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [currentUser, setCurrentUser] = useState<User | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    async function signup(email: string, password: string){
        return await createUserWithEmailAndPassword(auth, email, password);
    }

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, user => {
            setCurrentUser(user);
            setLoading(false);
        });

        return () => {
            unsubscribe();
        };
    }, []);

    const value = {
        currentUser,
        signup
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
}
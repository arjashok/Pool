import React, {useRef, useState} from "react";
import { Form, Button, Card, Alert } from "react-bootstrap";
import { useAuth } from "../contexts/AuthContext";

export default function Signup() {
    const emailRef = useRef<HTMLInputElement>(null);
    const passwordRef = useRef<HTMLInputElement>(null);
    const passwordConfirmRef = useRef<HTMLInputElement>(null);
    const { signup, currentUser } = useAuth();
    const [error, setError] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);

    async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();

        if (passwordRef.current!.value !== passwordConfirmRef.current!.value){
            return setError("Passwords do not match");
        }
        try {
            setError("");
            setLoading(true);
            await signup(emailRef.current!.value, passwordRef.current!.value);
        }
        catch {
            setError("Failed to create an account");
        }
        setLoading(false);
    }

    return (
        <div>
            <Card>
                <Card.Body>
                    <h2 className="text-center mb-4">Sign Up</h2>
                    {currentUser && currentUser.email}
                    {error && <Alert variant="danger">{error}</Alert>}
                    <Form onSubmit={handleSubmit}>
                        <Form.Group className="mt-2" id="email">
                            <Form.Label> Email </Form.Label>
                            <Form.Control type="email" ref = {emailRef} required />
                        </Form.Group>
                        <Form.Group className="mt-2" id="password">
                            <Form.Label> Password </Form.Label>
                            <Form.Control type="password" ref = {passwordRef} required />
                        </Form.Group>
                        <Form.Group className="mt-2" id="password-confirm">
                            <Form.Label> Password Confirmation </Form.Label>
                            <Form.Control type="password" ref = {passwordConfirmRef} required />
                        </Form.Group>
                        <Button disabled={loading} className="w-100 mt-4" type="submit">Sign Up</Button>
                    </Form>
                </Card.Body>
            </Card>
            <div className="w-100 text-center mt-2">
                Already have an account? Log in
            </div>
        </div>
    );
}
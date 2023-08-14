import React, {useRef, useState} from "react";
import { Form, Button, Card, Alert } from "react-bootstrap";
import { useAuth } from "../contexts/AuthContext";
import { Link, useNavigate, Navigate } from "react-router-dom"; 

export default function UpdateProfile() {
    const emailRef = useRef<HTMLInputElement>(null);
    const oldPasswordRef = useRef<HTMLInputElement>(null);
    const passwordRef = useRef<HTMLInputElement>(null);
    const passwordConfirmRef = useRef<HTMLInputElement>(null);
    const { currentUser, emailUpdate, passwordUpdate } = useAuth();
    const [error, setError] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const navigate = useNavigate();

    if (!currentUser) {
        return <Navigate to="/login" />;
    }

    function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();

        setError("");
        setLoading(true);

        if (passwordRef.current!.value !== passwordConfirmRef.current!.value){
            return setError("Passwords do not match");
        }

        const promises = []
        if (passwordRef.current!.value) {
            promises.push(passwordUpdate(oldPasswordRef.current!.value, passwordRef.current!.value));
        }
        if (emailRef.current!.value !== currentUser?.email) {
            promises.push(emailUpdate(emailRef.current!.value));
        }

        Promise.all(promises).then(() => {
            navigate("/");
        }).catch(() => {
            setError("Failed to update account");
        }).finally(() => {
            setLoading(false);
        });
        setLoading(false);
    }

    return (
        <div>
            <Card>
                <Card.Body>
                    <h2 className="text-center mb-4">Update Profile</h2>
                    {error && <Alert variant="danger">{error}</Alert>}
                    <Form onSubmit={handleSubmit}>
                        <Form.Group className="mt-2" id="email">
                            <Form.Label> Email </Form.Label>
                            <Form.Control type="email" ref = {emailRef} required defaultValue={currentUser?.email || ""} />
                        </Form.Group>
                        <Form.Group className="mt-2" id="password">
                            <Form.Label> Current Password </Form.Label>
                            <Form.Control type="password" ref = {oldPasswordRef} placeholder="Leave blank if not changing password"/>
                        </Form.Group>
                        <Form.Group className="mt-2" id="password">
                            <Form.Label> New Password </Form.Label>
                            <Form.Control type="password" ref = {passwordRef} placeholder="Leave blank to keep the same"/>
                        </Form.Group>
                        <Form.Group className="mt-2" id="password-confirm">
                            <Form.Label> Password Confirmation </Form.Label>
                            <Form.Control type="password" ref = {passwordConfirmRef} placeholder="Leave blank to keep the same" />
                        </Form.Group>
                        <Button disabled={loading} className="w-100 mt-4" type="submit">Update</Button>
                    </Form>
                </Card.Body>
            </Card>
            <div className="w-100 text-center mt-2">
                <Link to="/">Cancel</Link>
            </div>
        </div>
    );
}
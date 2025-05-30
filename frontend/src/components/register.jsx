import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./login.css";

function Register() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!name || !email || !password) {
      setMessage("❌ Please fill in all fields.");
    } else {
      setMessage(`✅ Registered successfully as ${name}`);
    }
  };

  return (
    <div className="form-container">

                <h1 className="logo">the second mind.</h1>
        <div className="fancy-border">

      <form className="form reg" onSubmit={handleSubmit}>
        <h2>Register</h2>

        <label>Name:</label>
        <input
          type="text"
          value={name}
          placeholder="Enter your name"
          onChange={(e) => setName(e.target.value)}
          required
          />

        <label>Email:</label>
        <input
          type="email"
          value={email}
          placeholder="Enter your email"
          onChange={(e) => setEmail(e.target.value)}
          required
          />

        <label>Password:</label>
        <input
          type={showPassword ? "text" : "password"}
          value={password}
          placeholder="Create a password"
          onChange={(e) => setPassword(e.target.value)}
          required
          />

        <div className="checkbox-container">
          <input
            type="checkbox"
            id="showPasswordRegister"
            checked={showPassword}
            onChange={() => setShowPassword(!showPassword)}
            />
          <label htmlFor="showPasswordRegister">Show Password</label>
        </div>

        <button type="submit" className="log-button">Register</button>

        <button type="button" className="switch-button" onClick={() => navigate("/login")}>
          Already have an account? Login
        </button>

        {message && <p className="message">{message}</p>}
      </form>
            </div>
    </div>
  );
}

export default Register;



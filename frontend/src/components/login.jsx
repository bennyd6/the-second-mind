import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./login.css";

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (email === "admin@example.com" && password === "123456") {
      setMessage("✅ Login successful!");
    } else {
      setMessage("❌ Invalid email or password.");
    }
  };

  return (
      <div className="log-main">

    <div className="form-container">
        <h1 className="logo">the second mind.</h1>
        <div className="fancy-border">
      <form className="form" onSubmit={handleSubmit}>
        <h2>Login</h2>

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
          placeholder="Enter your password"
          onChange={(e) => setPassword(e.target.value)}
          required
          />

        <div className="checkbox-container">
          <input
            type="checkbox"
            id="showPasswordLogin"
            checked={showPassword}
            onChange={() => setShowPassword(!showPassword)}
            />
          <label htmlFor="showPasswordLogin">Show Password</label>
        </div>

        <button type="submit" className="log-button">Login</button>

        <button type="button" className="switch-button" onClick={() => navigate("/register")}>
          Don’t have an account? Register
        </button>

        {message && <p className="message">{message}</p>}
      </form>
        </div>
    </div>
    </div>
  );
}

export default Login;
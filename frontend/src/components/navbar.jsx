import './navbar.css';
import home from '../assets/home.png'

export default function Navbar() {
    return (
        <div className="nav-main">
        {/* <div className="nav-mask"></div> */}
        <div className="nav-1">
            <a href="/">
            <img src={home} alt="" />
            </a>
        </div>
        <h1>the second mind.</h1>
        <div className="nav-2">
            <a href="/history">History</a>
            <a href="/login">Logout</a>
        </div>
        </div>
    );
}

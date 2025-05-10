import { useEffect, useState } from 'react';
import './home.css';
import Navbar from './navbar';
import Lp from './lp';
import Content from './content';

export default function Home() {
    const [showSplash, setShowSplash] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            setShowSplash(false);
        }, 2000);

        return () => clearTimeout(timer);
    }, []);

    return (
        <div className="main">
            {showSplash ? (
                <div className="splash splash-exit">
                    <h1>The Second Mind</h1>
                </div>
            ) : (
                <div className="main-2 main-2-enter">
                    <Navbar>

                    </Navbar>
                    <div className="main-2-in">
                        <Lp></Lp>
                        <Content></Content>
                    </div>
                </div>
            )}
        </div>
    );
}

import './content.css';
import Bg from '../assets/bg1.mp4';
import Content1 from './content-1';
import Content2 from './content-2';
import Loader from './loader';

export default function Content() {
    return (
        <div className="cont-main">
            <div className="cont-in">
                <video className="bg-video" autoPlay muted loop>
                    <source src={Bg} type="video/mp4" />
                    Your browser does not support the video tag.
                </video>
                <div className="overlay"></div>
                <Content1></Content1>
                {/* <Content2></Content2> */}
                {/* <Loader></Loader> */}
            </div>
        </div>
    );
}

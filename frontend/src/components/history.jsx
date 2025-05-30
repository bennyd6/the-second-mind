import './history.css'
import Bg from '../assets/bg1.mp4'

export default function History(){
    return(
        <>
        <div className="his-main">
            <div className="his-in">

            <video className="bg-video his-vid" autoPlay muted loop>
                <source src={Bg} type="video/mp4" />
                Your browser does not support the video tag.
            </video>
            {/* <div className="overlay his-overlay"></div> */}
            </div>
        </div>
        </>
    )
}
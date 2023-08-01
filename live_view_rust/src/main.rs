// using code from https://blog.devgenius.io/rust-and-opencv-bb0467bf35ff for live video feed
//error on M1 Macbook Pro: "dyld[44378]: Library not loaded: @rpath/libclang.dylib"
//solution: export DYLD_FALLBACK_LIBRARY_PATH="$(xcode-select --print-path)/usr/lib/"
//for other troubleshooting: https://github.com/twistedfall/opencv-rust
//system command documentation: https://doc.rust-lang.org/std/process/struct.Command.html
use anyhow::Result;
use opencv::{
    prelude::*,
    videoio,
    highgui
};
use std::process::Command;

fn camera_config() {
    //configure camera settings, equivalent to camera_config() in video_view.py
    //need to have each argument in different .arg function
    let mut focus_automatic = Command::new("v4l2-ctl");
    focus_automatic.arg("--device")
            .arg("/dev/video0")
            .arg("--set-ctrl=focus_automatic_continuous=1");
    focus_automatic.status().expect("process failed to execute");

    let mut white_balance = Command::new("v4l2-ctl");
    white_balance.arg("--device")
            .arg("/dev/video0")
            .arg("--set-ctrl=white_balance_automatic=1");
    white_balance.status().expect("process failed to execute");

    /*
    let mut temperature = Command::new("v4l2-ctl");
    temperature.arg("--device")
            .arg("/dev/video0")
            .arg("--set-ctrl=white_balance_temperature=4600");
    temperature.status().expect("process failed to execute");
    */
    //commenting out for now, as white balance is already automatic. 
    //System says "white_balance_temperature: permission denied" when trying to manually set temperature while white balance is automatic. This is expected.

    let mut exposure = Command::new("v4l2-ctl");
    exposure.arg("--device")
            .arg("/dev/video0")
            .arg("--set-ctrl=auto_exposure=1");
    exposure.status().expect("process failed to execute");

    println!("Camera Config: Complete");
}

fn main() -> Result<()>{ //this is anyhow::Result
    //Open a GUI Window
    camera_config();
    highgui::named_window("window", highgui::WINDOW_FULLSCREEN)?;
    //open webcam 
    let mut cam = videoio::VideoCapture::new(0, videoio::CAP_ANY)?;
    let mut frame = Mat::default(); // This array will store web-cam data
    //read the camera
    //then display in the window
    loop {
        cam.read(&mut frame)?;
        highgui::imshow("window", &frame)?;
        let key = highgui::wait_key(1)?;
        if key == 113 { //quit by pressing 'q'
            break;
        }

    }
    Ok(())
}

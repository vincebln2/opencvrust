use anyhow::Result;
use opencv::{
    prelude::*,
    videoio,
    highgui,
};
use std::process::Command;

fn camera_config() {
    //configure camera settings, equivalent to camera_config() in video_view.py
    //need to have each argument of command in different .arg function
    println!("Camera Config: Starting...");
    //note: camera firmware is LYING about its values 
    //(attempt to) set white balance, focus, and exposure
    let mut controls = Command::new("v4l2-ctl");
    controls.arg("--device")
            .arg("/dev/video0")
            .arg("--set-ctrl=white_balance_automatic=0")
            .arg("--set-ctrl=white_balance_temperature=4600")
            //temp range: 2800-6500
            .arg("--set-ctrl=auto_exposure=1")
            .arg("--set-ctrl=focus_automatic_continuous=0")
            .arg("--set-ctrl=focus_absolute=480");
    controls.status().expect("process failed to execute");
    println!("Camera Config: Complete");
}

fn main() -> Result<()> {
    //camera_config();
    //change settings of video recording
    let fps: f64 = 30.0;
    let num_frames = 150;
    let frame_width = 640;
    let frame_height =  480;
    let file_name = "./bleh.mp4";
    //480p: 640 width x 480 height
    //1080p: 1920 width x 1020 height
    //4k: 3840 width x 2080 height
    let mut cam = opencv::videoio::VideoCapture::new(0, videoio::CAP_ANY)?;
    //VideoWriter and VideoCapture use the fourcc data type to set the encoder format. 
    //fourcc parameters require 4 separate characters, tldr: "mjpg" does not work, 'm' 'j' 'p' 'g' does work
    let fourcc = opencv::videoio::VideoWriter::fourcc(
        'M' as char,
        'J' as char,
        'P' as char,
        'G' as char,
    )?;
    //You need to explicitly set the encoder and frame width and height here as well.
    videoio::VideoCapture::set(&mut cam, videoio::CAP_PROP_FOURCC, fourcc.into())?;
    videoio::VideoCapture::set(&mut cam, videoio::CAP_PROP_FRAME_WIDTH, frame_width.into())?;
    videoio::VideoCapture::set(&mut cam, videoio::CAP_PROP_FRAME_HEIGHT, frame_height.into())?;
    let mut frame = Mat::default();
    
    let mut vid = opencv::videoio::VideoWriter::new(
        file_name, //name of file
        fourcc,
        fps.into(),
        (frame_width, frame_height).into(),
        true
    ).expect("Can not open video writer");

    //read before config, first read resets (not sure? camera firmware is acting odd)

    cam.read(&mut frame)?;
    camera_config();
    for n in 1..num_frames {
        cam.read(&mut frame)?;
        vid.write(&frame)?;
        println!("{}", n);
        let key = highgui::wait_key(1)?;
        if key == 113 { //quit by pressing 'q'
            break;
        }
    }

Ok(())
}


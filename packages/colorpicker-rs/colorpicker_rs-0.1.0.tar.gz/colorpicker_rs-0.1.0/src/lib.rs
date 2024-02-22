use reqwest::blocking::get;
use pyo3::prelude::*;
use image::Pixel;

#[pyfunction]
fn get_dominant_color(_py: Python, url: &str) -> PyResult<String> {
    // Fetch image data from URL
    // Fetch image data from URL
    // Fetch image data from URL
    let response = get(url).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to fetch image: {}", e))
    })?;

    let bytes = response.bytes().map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to read image data: {}", e))
    })?;

    // Decode image data
    let img = image::load_from_memory(&bytes)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Error decoding image: {}", e)))?;

    // Resize the image
    let resized_img = image::imageops::resize(&img, 100, 100, image::imageops::FilterType::Lanczos3);

    // Calculate mean RGB values
    let (mut r_sum, mut g_sum, mut b_sum) = (0, 0, 0);
    let pixel_count = resized_img.width() * resized_img.height();
    for pixel in resized_img.pixels() {
        let channels = pixel.channels();
        r_sum += channels[0] as u32;
        g_sum += channels[1] as u32;
        b_sum += channels[2] as u32;
    }

    // Calculate mean RGB values
    let r_mean = r_sum / pixel_count;
    let g_mean = g_sum / pixel_count;
    let b_mean = b_sum / pixel_count;

    // Convert to hex string
    let hex_color = format!("#{:02X}{:02X}{:02X}", r_mean, g_mean, b_mean);

    Ok(hex_color)
}

#[pymodule]
fn colorpicker_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_dominant_color, m)?)?;
    Ok(())
}

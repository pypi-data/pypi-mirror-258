use http::Uri;
use prism_client::{AsyncClient, Wavelet};

async fn print_wavelet(wavelet: Wavelet) {
    println!(
        "Wavelet {} (n_messages: {})",
        wavelet.beam,
        wavelet.photons.len()
    );
}

async fn run_client(addr: &str) -> std::io::Result<()> {
    let uri = addr.parse::<Uri>().unwrap();
    let mut client = AsyncClient::connect(uri, print_wavelet)
        .await
        .map_err(|_| std::io::Error::new(std::io::ErrorKind::Other, "Connection failure"))?;

    client.subscribe("beam1".to_string(), None).await.unwrap();
    let payload = vec![0, 1, 2, 3];
    loop {
        client
            .emit("beam1".to_string(), payload.clone())
            .await
            .unwrap();
    }
}

fn setup_tracing() {
    let subscriber = tracing_subscriber::fmt()
        .compact()
        .with_level(true)
        .with_thread_ids(true)
        .with_line_number(true)
        .with_file(true)
        .with_max_level(tracing::Level::DEBUG)
        .finish();
    tracing::subscriber::set_global_default(subscriber).expect("Could not set up tracing");
}

#[tokio::main(flavor = "multi_thread", worker_threads = 4)]
async fn main() -> std::io::Result<()> {
    setup_tracing();
    run_client("ws://127.0.0.1:5050").await?;
    Ok(())
}

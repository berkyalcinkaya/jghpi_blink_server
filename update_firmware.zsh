#!/bin/bash

# URL and output file name for the first download
URL1="https://static.onlogic.com/resources/firmware/utilities/zmu-1.0.0.zip?_gl=1*1afva2y*_gcl_aw*R0NMLjE3MjA1Mzk3NDEuQ2owS0NRand2N08wQmhEd0FSSXNBQzBzaldPX1QzbjY2NFZPcUJ3YUY2TVBnR1Y4bm55QUxFRDgzdkRkX2VSV2I2eGtZcW0xdjRDZENib2FBa1NVRUFMd193Y0I.*_gcl_au*MTczODYzODcxNC4xNzE4NjMzOTc4*_ga*MTI0OTM1MTA4Ni4xNzE4NjMzOTc3*_ga_SEVJD5HQBB*MTcyMjI2NDU3NC4xMi4xLjE3MjIyNjQ3MDkuNjAuMC4w"
OUTPUT1="zmu-1.0.0.zip"

# URL and output file name for the second download
URL2="https://static.onlogic.com/resources/firmware/binaries/FR202/fr202_dio_v1.3.1.0.app.bin?_gl=1*1rxynle*_gcl_aw*R0NMLjE3MjA1Mzk3NDEuQ2owS0NRand2N08wQmhEd0FSSXNBQzBzaldPX1QzbjY2NFZPcUJ3YUY2TVBnR1Y4bm55QUxFRDgzdkRkX2VSV2I2eGtZcW0xdjRDZENib2FBa1NVRUFMd193Y0I.*_gcl_au*MTczODYzODcxNC4xNzE4NjMzOTc4*_ga*MTI0OTM1MTA4Ni4xNzE4NjMzOTc3*_ga_SEVJD5HQBB*MTcyMjI2NDU3NC4xMi4xLjE3MjIyNjQ3MDkuNjAuMC4w"
OUTPUT2="fr202_dio_v1.3.1.0.app.bin"

# Function to download a file using curl
download_file() {
    local url=$1
    local output=$2
    echo "Downloading $output..."
    curl -o "$output" "$url"
    if [[ $? -ne 0 ]]; then
        echo "Failed to download $output"
        exit 1
    fi
    echo "Downloaded $output successfully."
}

# Function to unzip a file
unzip_file() {
    local file=$1
    local output_dir=$2
    if [[ $file == *.zip ]]; then
        echo "Unzipping $file..."
        unzip "$file" -d "$output_dir"
        if [[ $? -ne 0 ]]; then
            echo "Failed to unzip $file"
            exit 1
        fi
        echo "Unzipped $file successfully."
    else
        echo "$file is not a zip file, skipping unzip."
    fi
}

# Download files
download_file "$URL1" "$OUTPUT1"
download_file "$URL2" "$OUTPUT2"

# Unzip the first downloaded file
unzip_file "$OUTPUT1" "$HOME/Downloads"

# Define the ZMU utility variable
zmu="zmu-linux-$(uname -m)"

# Make the ZMU utility executable
chmod +x "$HOME/Downloads/$zmu"

# Run the ZMU utility with the firmware binary
sudo "$HOME/Downloads/$zmu" image upload "$OUTPUT2"

# Instruct the user to shut down the computer
echo "Once the update is complete, fully shutdown the computer (not just a 
Restart). Turn the system back on, and the update is now complete."

echo "All tasks completed successfully."


const Jimp = require('jimp');

async function processImage() {
  try {
    const inputPath = "C:\\Users\\LENOVO\\.gemini\\antigravity\\brain\\8b1ace12-cd8f-4b85-b571-47bfdf268ed7\\.user_uploaded\\media_1786723432929.png";
    const outputPath = "e:\\TBD\\company wise dsa\\frontend\\public\\favicon.png";
    
    console.log("Loading image...");
    const image = await Jimp.read(inputPath);
    
    console.log("Autocropping image...");
    // autocrop removes surrounding solid background color
    image.autocrop();
    
    // Resize to a square of 256x256 to ensure it's standard and proportionate
    image.contain(256, 256);
    
    console.log("Saving image...");
    await image.writeAsync(outputPath);
    console.log("Saved cropped image to " + outputPath);
  } catch (err) {
    console.error("Error processing image:", err);
  }
}

processImage();

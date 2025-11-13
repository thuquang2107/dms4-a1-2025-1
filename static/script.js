// /astro-numero-app/frontend/script.js

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('birthdate-form');
    const inputSection = document.getElementById('input-section');
    const resultSection = document.getElementById('result-section');
    const loadingSpinner = document.getElementById('loading');
    const card = document.getElementById('prediction-card');

    // --- p5.js Sketch for Background Animation ---
    let stars = [];

   // --- Bắt đầu sketch p5.js ---

// --- Bắt đầu sketch p5.js ---

const sketch = (p) => {
    // Các biến cho hiệu ứng nền (Code 1)
    let stars = [];

    // Các biến cho hiệu ứng tiền cảnh (Code 2)
    let pg; // Lớp đồ họa (graphic layer) để vẽ hoa văn nhiễu
    let r = 0; // Bán kính
    let t = 0; // Biến thời gian cho nhiễu

    p.setup = () => {
        let canvas = p.createCanvas(p.windowWidth, p.windowHeight);
        // Nếu bạn có một thẻ div cụ thể, hãy dùng dòng này:
        canvas.parent('p5-canvas-container');

        // --- Thiết lập cho Nền (Code 1) ---
        for (let i = 0; i < 800; i++) {
            stars[i] = new Star(p);
        }

        // --- Thiết lập cho Tiền cảnh (Code 2) ---
        // Tạo một canvas phụ (off-screen) có cùng kích thước
        pg = p.createGraphics(p.windowWidth, p.windowHeight);
    };

    p.draw = () => {
        // --- 1. Vẽ Nền không tương tác (Code 1) ---
        p.background(26, 26, 46); // Nền màu xanh đậm
        p.translate(p.width / 2, p.height / 2); // Di chuyển gốc tọa độ vào giữa cho hiệu ứng sao
        for (let i = 0; i < stars.length; i++) {
            stars[i].update(p);
            stars[i].show(p);
        }
        // Đặt lại ma trận biến đổi để các hình vẽ tiếp theo không bị ảnh hưởng
        p.resetMatrix();

        // --- 2. Cập nhật và vẽ Tiền cảnh tương tác (Code 2) ---
        // Vẽ một lớp nền bán trong suốt lên canvas phụ để tạo hiệu ứng mờ dần
        pg.background(26, 26, 46, 25);
        pg.stroke(255); // Đặt màu cho các điểm là màu trắng
        pg.strokeWeight(1.5); // Làm cho các điểm dày hơn một chút

        // Vòng lặp để tạo ra hoa văn nhiễu
        for (let i = 0; i < 3000; i++) {
            // Tính toán góc và bán kính
            let a = p.noise(i % 64.0) * 9 + t / r;
            // Bán kính phụ thuộc vào vị trí X của chuột (tương tác)
            r = p.abs(p.noise(i) - 0.2) * p.mouseX;

            // Vẽ một điểm lên canvas phụ tại vị trí tương đối so với tâm
            pg.point(p.width / 2 + p.cos(a) * r, p.height / 2 + p.sin(a) * r / 2.0);
        }
        t += 0.001; // Cập nhật biến thời gian để hoa văn chuyển động

        // --- 3. Vẽ canvas phụ lên canvas chính ---
        p.image(pg, 0, 0);
    };

    p.windowResized = () => {
        p.resizeCanvas(p.windowWidth, p.windowHeight);
        // Đảm bảo canvas phụ cũng được thay đổi kích thước
        pg.resizeCanvas(p.windowWidth, p.windowHeight);
    };

    // Lớp Star từ Code 1 (không thay đổi)
    class Star {
        constructor(p) {
            this.x = p.random(-p.width, p.width);
            this.y = p.random(-p.height, p.height);
            this.z = p.random(p.width);
            this.pz = this.z;
        }

        update(p) {
            this.z = this.z - 10;
            if (this.z < 1) {
                this.z = p.width;
                this.x = p.random(-p.width, p.width);
                this.y = p.random(-p.height, p.height);
                this.pz = this.z;
            }
        }

        show(p) {
            p.fill(255);
            p.noStroke();

            const sx = p.map(this.x / this.z, 0, 1, 0, p.width);
            const sy = p.map(this.y / this.z, 0, 1, 0, p.height);
            const r = p.map(this.z, 0, p.width, 16, 0);
            p.ellipse(sx, sy, r, r);
        }
    }
};

new p5(sketch);
// --- Kết thúc sketch p5.js ---
// --- Kết thúc sketch p5.js ---
    function initP5Sketch(videoUrl) {
    const sketch = (p) => {
        let vid;

        p.setup = () => {
            let canvas = p.createCanvas(p.windowWidth, p.windowHeight, p.WEBGL);
            canvas.parent('p5-canvas-container'); // Gắn canvas vào div có sẵn
            
            // Tạo video từ URL nhận được
            vid = p.createVideo([videoUrl]);
            vid.loop(); // Lặp lại video
            vid.volume(0); // Tắt tiếng video
            vid.hide(); // Ẩn element video gốc
        };

        p.draw = () => {
            p.background(10); // Background đen nếu video chưa tải xong
            
            // Map vị trí chuột để tạo góc xoay
            // Giới hạn góc xoay để hiệu ứng nhẹ nhàng, không bị lật ngược
            let rotY = p.map(p.mouseX, 0, p.width, -p.PI / 8, p.PI / 8);
            let rotX = p.map(p.mouseY, 0, p.height, p.PI / 12, -p.PI / 12);
            
            p.push(); // Bắt đầu một trạng thái vẽ mới
            p.rotateX(rotX);
            p.rotateY(rotY);
            
            // Áp video làm texture cho mặt phẳng
            p.texture(vid);
            p.noStroke(); // Bỏ đường viền
            
            // Kích thước của mặt phẳng chứa video
            // Tỷ lệ 16:9 phổ biến
            const videoWidth = p.width * 1.5; // Phóng to để video luôn tràn viền
            const videoHeight = (videoWidth * 9) / 16;
            p.plane(videoWidth, videoHeight);
            
            p.pop(); // Phục hồi trạng thái vẽ
        };

        p.windowResized = () => {
            p.resizeCanvas(p.windowWidth, p.windowHeight);
        };
    };

    new p5(sketch);
}

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const birthdate = document.getElementById('birthdate').value;
        if (!birthdate) return;

        // Show loading spinner
        inputSection.classList.add('hidden');
        loadingSpinner.classList.remove('hidden');
        resultSection.classList.add('hidden');
        card.classList.remove('is-flipped'); // Reset card flip

        try {
            // Fetch prediction from the backend API
            const response = await fetch('/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ birthdate: birthdate }),
});


            if (!response.ok) {
                throw new Error('Failed to get prediction');
            }

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            console.error('Error:', error);
            alert('Could not retrieve your forecast. Please try again later.');
            inputSection.classList.remove('hidden'); // Show input form again
        } finally {
            // Hide loading spinner
            loadingSpinner.classList.add('hidden');
        }
    });

    // Handle card flip
    card.addEventListener('click', () => {
        card.classList.toggle('is-flipped');
    });

    // Function to update the UI with the fetched data
    function displayResults(data) {
    document.getElementById('apod-image').src = data.prediction_image_url;
    
    document.getElementById('life-path-header').innerText = `Your life path is ${data.life_path_number}`;
    
    // === DÒNG MỚI ĐƯỢC THÊM VÀO ===
    // Lấy dữ liệu character từ backend và hiển thị
    document.getElementById('character-description').innerText = data.character_description;
    
    // Dòng này bây giờ sẽ hiển thị lời khuyên hàng ngày
    document.getElementById('daily-advice').innerText = data.daily_advice;
    
    document.getElementById('astro-insight').innerText = data.astronomical_insight;
    
    const colorSwatch = document.getElementById('lucky-color');
    colorSwatch.style.backgroundColor = data.lucky_color.toLowerCase(); // Chuyển sang chữ thường để CSS nhận diện màu
    colorSwatch.innerText = data.lucky_color;
    
    resultSection.classList.remove('hidden');
}

});

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const formWrapper = document.querySelector('.form-wrapper');
    const resultContainer = document.getElementById('result-container');
    const predictedRatingSpan = document.getElementById('predicted-rating');
    const resetBtn = document.getElementById('reset-btn');
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loader, hide text
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');

        // Gather data
        const payload = {
            year: document.getElementById('year').value,
            duration: document.getElementById('duration').value,
            genre: document.getElementById('genre').value,
            votes: document.getElementById('votes').value,
            director: document.getElementById('director').value,
            actor1: document.getElementById('actor1').value,
            actor2: document.getElementById('actor2').value,
            actor3: document.getElementById('actor3').value
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (data.success) {
                // Animate Out Form
                formWrapper.style.transform = 'translateY(-20px)';
                formWrapper.style.opacity = '0';
                
                setTimeout(() => {
                    formWrapper.classList.add('hidden');
                    
                    // Set Result and Animate In
                    predictedRatingSpan.textContent = data.prediction.toFixed(1);
                    resultContainer.classList.remove('hidden');
                    resultContainer.style.animation = 'none'; // reset animation
                    void resultContainer.offsetWidth; // trigger reflow
                    resultContainer.style.animation = 'zoomIn 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards';
                    
                }, 500);
            } else {
                alert('Prediction Error: ' + (data.error || 'Unknown error'));
            }
        } catch (err) {
            console.error(err);
            alert('Failed to connect to the prediction server. Please make sure the backend is running.');
        } finally {
            // Restore button state
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
        }
    });

    resetBtn.addEventListener('click', () => {
        // Animate Out Result
        resultContainer.style.transform = 'scale(0.8)';
        resultContainer.style.opacity = '0';
        
        setTimeout(() => {
            resultContainer.classList.add('hidden');
            resultContainer.style.transform = '';
            resultContainer.style.opacity = '';
            
            // Re-show form
            form.reset();
            formWrapper.classList.remove('hidden');
            formWrapper.style.animation = 'none';
            void formWrapper.offsetWidth;
            formWrapper.style.animation = 'fadeInUp 1s ease forwards';
        }, 400);
    });
});

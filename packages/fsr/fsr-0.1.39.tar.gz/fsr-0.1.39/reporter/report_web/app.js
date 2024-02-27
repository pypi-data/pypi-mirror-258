function showTestDetails(test) {
    const mainContentElement = document.getElementById('main-content');
    mainContentElement.innerHTML = '';

    const testNameElement = document.createElement('h2');
    testNameElement.textContent = `${test.name} - ${test.result === 'success' ? 'PASSED' : 'FAILED'}`;
    mainContentElement.appendChild(testNameElement);

    const imagesContainer = document.createElement('div');
    imagesContainer.style.display = 'flex';
    imagesContainer.style.justifyContent = 'space-around';
    imagesContainer.style.marginTop = '20px';

    const createModalImage = (src) => {
        const modal = document.createElement('div');
        modal.style.position = 'fixed';
        modal.style.top = '0';
        modal.style.left = '0';
        modal.style.width = '100%';
        modal.style.height = '100%';
        modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        modal.style.display = 'flex';
        modal.style.justifyContent = 'center';
        modal.style.alignItems = 'center';
        modal.style.zIndex = '1000';
        modal.addEventListener('click', () => modal.remove());

        const modalImg = document.createElement('img');
        modalImg.src = src;
        modalImg.style.maxWidth = '90%';
        modalImg.style.maxHeight = '90%';
        modal.appendChild(modalImg);

        document.body.appendChild(modal);
    };

    if (test.images.goldens.length > 0) {
        const goldensContainer = document.createElement('div');
        const goldensTitle = document.createElement('h3');
        goldensTitle.textContent = 'Goldens';
        goldensContainer.appendChild(goldensTitle);

        test.images.goldens.forEach(image => {
            const imageName = image.split('\\').pop();
            const imageElement = document.createElement('img');
            imageElement.src = image.replace(/\\/g, '/');
            imageElement.style.maxWidth = '100px';
            imageElement.alt = imageName;
            imageElement.style.cursor = 'pointer';
            imageElement.onclick = () => createModalImage(imageElement.src);
            const imageTitle = document.createElement('p');
            imageTitle.textContent = imageName;
            goldensContainer.appendChild(imageTitle);
            goldensContainer.appendChild(imageElement);
        });

        imagesContainer.appendChild(goldensContainer);
    }

    if(test.result !== 'success' && test.images.failures && test.images.failures.length > 0) {
        const failuresContainer = document.createElement('div');
        const failuresTitle = document.createElement('h3');
        failuresTitle.textContent = 'Failures';
        failuresContainer.appendChild(failuresTitle);

        test.images.failures.forEach(image => {
            const imageName = image.split('\\').pop();
            const imageElement = document.createElement('img');
            imageElement.src = image.replace(/\\/g, '/');
            imageElement.style.maxWidth = '100px';
            imageElement.alt = imageName;
            imageElement.style.cursor = 'pointer';
            imageElement.onclick = () => createModalImage(imageElement.src);
            const imageTitle = document.createElement('p');
            imageTitle.textContent = imageName;
            failuresContainer.appendChild(imageTitle);
            failuresContainer.appendChild(imageElement);
        });

        imagesContainer.appendChild(failuresContainer);
    }

    mainContentElement.appendChild(imagesContainer);

    const logsTitle = document.createElement('h3');
    logsTitle.textContent = 'Logs';
    const logsContainer = document.createElement('div');
    logsContainer.style.marginTop = '20px';
    logsContainer.style.padding = '10px';
    logsContainer.style.backgroundColor = '#f0f0f0';
    logsContainer.style.borderRadius = '5px';
    logsContainer.style.maxHeight = '200px';
    logsContainer.style.overflowY = 'scroll';
    test.messages.forEach(log => {
        const logElement = document.createElement('p');
        logElement.textContent = log;
        logsContainer.appendChild(logElement);
    });
    mainContentElement.appendChild(logsTitle);
    mainContentElement.appendChild(logsContainer);
}

function showSummary() {
    const mainContentElement = document.getElementById('main-content');
    mainContentElement.innerHTML = '';

    fetch('data/data.json')
        .then(response => response.json())
        .then(data => {
            let passedTests = 0, failedTests = 0;
            const failedTestsList = [];
            data.forEach(test => {
                if (test.result === 'success') passedTests++;
                else {
                    failedTests++;
                    failedTestsList.push(test);
                }
            });

            const passedElement = document.createElement('h1');
            passedElement.textContent = `Passed tests: ${passedTests}`;
            passedElement.style.color = 'green';
            mainContentElement.appendChild(passedElement);

            const failedElement = document.createElement('h1');
            failedElement.textContent = `Failed tests: ${failedTests}`;
            failedElement.style.color = 'red';
            mainContentElement.appendChild(failedElement);

            if (failedTestsList.length > 0) {
                const failedTestsContainer = document.createElement('div');
                const failedTestsTitle = document.createElement('h2');
                failedTestsTitle.textContent = 'Failed tests list:';
                failedTestsContainer.appendChild(failedTestsTitle);

                failedTestsList.forEach(test => {
                    const testElement = document.createElement('li');
                    const linkElement = document.createElement('a');
                    linkElement.href = '#';
                    linkElement.textContent = test.name;
                    linkElement.onclick = () => showTestDetails(test);
                    testElement.appendChild(linkElement);
                    failedTestsContainer.appendChild(testElement);
                });

                mainContentElement.appendChild(failedTestsContainer);
            }
        });
}

document.addEventListener('DOMContentLoaded', () => {
    showSummary(); 

    fetch('data/data.json')
        .then(response => response.json())
        .then(data => {
            const testListElement = document.getElementById('test-list');
            data.forEach(test => {
                const testElement = document.createElement('li');
                const linkElement = document.createElement('a');
                linkElement.href = '#';
                linkElement.textContent = test.name;
                linkElement.onclick = () => showTestDetails(test);
                testElement.appendChild(linkElement);
                testListElement.appendChild(testElement);
            });
        });
});

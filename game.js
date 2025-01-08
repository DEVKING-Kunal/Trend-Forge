const nodes = document.querySelectorAll('.node');
const factDisplay = document.getElementById('fact-display');

nodes.forEach((node) => {
  node.addEventListener('click', () => {
    const fact = node.getAttribute('data-fact');
    factDisplay.textContent = fact;
  });
});

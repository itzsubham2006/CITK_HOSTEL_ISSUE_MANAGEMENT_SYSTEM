const container = document.getElementById("cube-container");

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b0f19);

const camera = new THREE.PerspectiveCamera(
  60,
  container.clientWidth / container.clientHeight,
  0.1,
  1000
);
camera.position.set(5, 5, 6);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// Lights
scene.add(new THREE.AmbientLight(0xffffff, 0.6));
const light = new THREE.DirectionalLight(0xffffff, 0.8);
light.position.set(5, 10, 7);
scene.add(light);

// Cube
const cubeGroup = new THREE.Group();
const colors = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0xffa500, 0xffffff];

for (let x = -1; x <= 1; x++) {
  for (let y = -1; y <= 1; y++) {
    for (let z = -1; z <= 1; z++) {
      const cube = new THREE.Mesh(
        new THREE.BoxGeometry(0.95, 0.95, 0.95),
        colors.map(c => new THREE.MeshStandardMaterial({ color: c }))
      );
      cube.position.set(x, y, z);
      cubeGroup.add(cube);
    }
  }
}

scene.add(cubeGroup);

// Resize fix
window.addEventListener("resize", () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}
animate();

window.resetCube = () => {
  cubeGroup.rotation.set(0, 0, 0);
};

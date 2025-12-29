document.addEventListener("DOMContentLoaded", () => {

  const dataEl = document.getElementById("hostelData");
  const roomMap = JSON.parse(dataEl.dataset.roomMap);
  const isStaff = dataEl.dataset.isStaff === "true";
  const capacity = parseInt(dataEl.dataset.capacity);

  const modal = document.getElementById("roomModal");
  const modalTitle = document.getElementById("modalRoomTitle");
  const modalContent = document.getElementById("modalContent");
  const addBtn = document.getElementById("addStudentBtn");

  document.querySelectorAll(".room").forEach(room => {
    room.onclick = () => openRoom(room.dataset.room);
  });

  document.getElementById("closeModal").onclick = () => {
    modal.style.display = "none";
  };

  function openRoom(roomNo) {
    modalTitle.innerText = `Room ${roomNo}`;
    const students = roomMap[roomNo] || [];

    if (students.length) {
      modalContent.innerHTML =
        "<ul>" +
        students.map(s => `<li>${s.name} (${s.email})</li>`).join("") +
        "</ul>";
    } else {
      modalContent.innerHTML = "<p>Room is empty</p>";
    }

    if (isStaff && students.length < capacity) {
      addBtn.style.display = "block";
      addBtn.onclick = () => {
        window.location.href = `/admin/add_student?room=${roomNo}`;
      };
    } else {
      addBtn.style.display = "none";
    }

    modal.style.display = "block";
  }
});

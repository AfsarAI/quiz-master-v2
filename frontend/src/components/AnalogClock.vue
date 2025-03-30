<template>
  <div class="clock-container">
    <canvas ref="clockCanvas" width="300" height="300"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from "vue";

export default {
  name: "AnalogClock",
  setup() {
    const clockCanvas = ref(null);
    let animationFrameId = null;

    const drawClock = (ctx) => {
      // Get time in Asia/Kolkata time zone
      const formatter = new Intl.DateTimeFormat("en-US", {
        timeZone: "Asia/Kolkata",
        hour: "numeric",
        minute: "numeric",
        second: "numeric",
        hour12: false,
      });

      const parts = formatter.formatToParts(new Date());
      const hour = parseInt(parts.find((p) => p.type === "hour").value) % 12;
      const minute = parseInt(parts.find((p) => p.type === "minute").value);
      const second = parseInt(parts.find((p) => p.type === "second").value);

      // Clear canvas
      ctx.clearRect(0, 0, 300, 300);

      // Draw clock face
      ctx.beginPath();
      ctx.arc(150, 150, 140, 0, 2 * Math.PI);
      ctx.fillStyle = "white";
      ctx.fill();
      ctx.strokeStyle = "#3498db";
      ctx.lineWidth = 8;
      ctx.stroke();

      // Draw hour marks
      for (let i = 0; i < 12; i++) {
        const angle = ((i - 3) * (Math.PI * 2)) / 12;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(150 + Math.cos(angle) * 120, 150 + Math.sin(angle) * 120);
        ctx.lineTo(150 + Math.cos(angle) * 140, 150 + Math.sin(angle) * 140);
        ctx.strokeStyle = "#3498db";
        ctx.stroke();
      }

      // Draw hour hand
      ctx.save();
      ctx.translate(150, 150);
      ctx.rotate(((hour + minute / 60) * Math.PI) / 6 - Math.PI / 2);
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.moveTo(-20, 0);
      ctx.lineTo(70, 0);
      ctx.strokeStyle = "#3498db";
      ctx.stroke();
      ctx.restore();

      // Draw minute hand
      ctx.save();
      ctx.translate(150, 150);
      ctx.rotate((minute * Math.PI) / 30 - Math.PI / 2);
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(-28, 0);
      ctx.lineTo(112, 0);
      ctx.strokeStyle = "#2980b9";
      ctx.stroke();
      ctx.restore();

      // Draw second hand
      ctx.save();
      ctx.translate(150, 150);
      ctx.rotate((second * Math.PI) / 30 - Math.PI / 2);
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(-30, 0);
      ctx.lineTo(120, 0);
      ctx.strokeStyle = "#e74c3c";
      ctx.stroke();
      ctx.restore();

      // Draw center circle
      ctx.beginPath();
      ctx.arc(150, 150, 5, 0, 2 * Math.PI);
      ctx.fillStyle = "#e74c3c";
      ctx.fill();
    };

    const animate = () => {
      const canvas = clockCanvas.value;
      const ctx = canvas.getContext("2d");
      drawClock(ctx);
      animationFrameId = requestAnimationFrame(animate);
    };

    onMounted(() => {
      animate();
    });

    onUnmounted(() => {
      cancelAnimationFrame(animationFrameId);
    });

    return {
      clockCanvas,
    };
  },
};
</script>

<style scoped>
.clock-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
</style>

import math
import tkinter as tk

class RotatingCube:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Wireframe Cube")
        
        # Setup Canvas
        self.width = 1200
        self.height = 800
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # 8 Vertices of a unit cube (x, y, z)
        self.vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1,  1]
        ]

        # 12 Edges connecting the corner vertices
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0), # Back face
            (4, 5), (5, 6), (6, 7), (7, 4), # Front face
            (0, 4), (1, 5), (2, 6), (3, 7)  # Connecting edges
        ]

        # Angles for rotation
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

        # Start animation loop
        self.update()

    def rotate_x(self, x, y, z, angle):
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        return x, y * cos_a - z * sin_a, y * sin_a + z * cos_a

    def rotate_y(self, x, y, z, angle):
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        return x * cos_a + z * sin_a, y, -x * sin_a + z * cos_a

    def rotate_z(self, x, y, z, angle):
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        return x * cos_a - y * sin_a, x * sin_a + y * cos_a, z

    def project(self, x, y, z):
        # Distance from camera to project 3D onto 2D screen
        distance = 3.5
        scale = 200
        
        # Perspective projection formula
        focal_length = distance / (distance + z)
        proj_x = x * focal_length * scale + self.width / 2
        proj_y = -y * focal_length * scale + self.height / 2
        return proj_x, proj_y

    def update(self):
        self.canvas.delete("all")

        # Increment rotation angles
        self.angle_x += 1.0
        self.angle_y += 1.5
        self.angle_z += 0.5

        transformed_vertices = []
        
        # Rotate and project each vertex
        for x, y, z in self.vertices:
            x, y, z = self.rotate_x(x, y, z, self.angle_x)
            x, y, z = self.rotate_y(x, y, z, self.angle_y)
            x, y, z = self.rotate_z(x, y, z, self.angle_z)
            
            px, py = self.project(x, y, z)
            transformed_vertices.append((px, py))

        # Draw lines connecting the projected corners
        for start_idx, end_idx in self.edges:
            x1, y1 = transformed_vertices[start_idx]
            x2, y2 = transformed_vertices[end_idx]
            self.canvas.create_line(x1, y1, x2, y2, fill="cyan", width=2)

        # Draw small circles on corners
        for px, py in transformed_vertices:
            self.canvas.create_oval(px - 3, py - 3, px + 3, py + 3, fill="white")

        # Loop around ~60 FPS
        self.root.after(16, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    app = RotatingCube(root)
    root.mainloop()
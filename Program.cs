using System.Numerics;
using Silk.NET.Maths;
using Silk.NET.OpenGL;
using Silk.NET.Windowing;
using TrippyGL;

using static Simulation;

namespace atomfg
{
    class Program
    {
        static IWindow        window;
        static GL             gl;
        static GraphicsDevice graphicsDevice;

        static VertexBuffer<VertexPosition> vertexBuffer;
        static SimpleShaderProgram          shaderProgram;

        static void Main(string[] args)
        {
            WindowOptions windowOpts = WindowOptions.Default;

            windowOpts.Title = "atomfg";
            windowOpts.API   = new GraphicsAPI(ContextAPI.OpenGL, ContextProfile.Core, ContextFlags.Debug, new APIVersion(3, 3));

            using IWindow nWindow = Window.Create(windowOpts);
            
            window = nWindow;

            window.Load    += Window_Load;
            window.Render  += Window_Render;
            window.Closing += Window_Closing;

            window.FramebufferResize += Window_FramebufferResize;

            window.Run();
        }

        private static void Window_Load()
        {
            gl             = window.CreateOpenGL();
            graphicsDevice = new GraphicsDevice(gl);

            Span<VertexPosition> sphere = stackalloc VertexPosition[]
            {
                new Vector3(0.0f, 1.0f, 0.0f),      // Top vertex
                new Vector3(1.0f, 0.0f, 0.0f),      // Right vertex
                new Vector3(0.0f, 0.0f, -1.0f),     // Front vertex
                new Vector3(-1.0f, 0.0f, 0.0f),     // Left vertex
                new Vector3(0.0f, 0.0f, 1.0f),      // Back vertex
                new Vector3(0.0f, -1.0f, 0.0f)      // Bottom vertex
            };

            vertexBuffer  = new VertexBuffer<VertexPosition>(graphicsDevice, sphere, BufferUsage.StaticDraw);
            shaderProgram = SimpleShaderProgram.Create<VertexColor>(graphicsDevice);

            Simulation.Simulate();

            Window_FramebufferResize(window.FramebufferSize);
        }

        private static void Window_Render(double dt)
        {
            graphicsDevice.ClearColor = Color4b.Black;
            graphicsDevice.Clear(ClearBuffers.Color);

            graphicsDevice.VertexArray   = vertexBuffer;
            graphicsDevice.ShaderProgram = shaderProgram;

            graphicsDevice.DrawArrays(TrippyGL.PrimitiveType.Triangles, 0, vertexBuffer.StorageLength);
        }

        private static void Window_FramebufferResize(Vector2D<int> size)
        {
            graphicsDevice.SetViewport(0, 0, (uint)size.X, (uint)size.Y);
        }

        private static void Window_Closing()
        {
            vertexBuffer.Dispose();
            shaderProgram.Dispose();
            graphicsDevice.Dispose();
            gl.Dispose();
        }
    }
}
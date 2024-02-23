#include <imgui-core/inc/imgui-modules.h>

#include <pybind11/functional.h>

#include <glad/gl.h>

#include <GLFW/glfw3.h>
#include <backends/imgui_impl_glfw.h>
#include <backends/imgui_impl_opengl3.h>

void GLFWErrCallback(int err, const char* msg)
{
    py::print("GLFW Error Code:", err, "Msg:", msg);
}

void* initGLFW(
    const char* title,
    int window_width,
    int window_height,
    int swap_interval = 1
)
{
    glfwSetErrorCallback(GLFWErrCallback);
    if(!glfwInit())
    {
        py::print("Cannot initialize GLFW");
        return nullptr;
    }

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 6);

    GLFWmonitor* primaryMonitor = glfwGetPrimaryMonitor();
    int width, height;
    glfwGetMonitorWorkarea(primaryMonitor, nullptr, nullptr, &width, &height);

    if(window_height == 0)
    {
        window_height = height;
    }
    if(window_width == 0)
    {
        window_width = width;
    }

    GLFWwindow* window =
        glfwCreateWindow(window_width, window_height, title, nullptr, nullptr);

    if(window == nullptr)
    {
        py::print("Cannot create GLFW window");
        return window;
    }

    glfwMakeContextCurrent(window);

    int version = gladLoadGL(glfwGetProcAddress);
    if(version == 0)
    {
        py::print("Failed to initialize the OpenGL context");
        glfwDestroyWindow(window);
        return nullptr;
    }

    glfwSwapInterval(swap_interval);

    return window;
}

void initContextForGLFW(void* window)
{
    GLFWwindow* gWindow = static_cast<GLFWwindow*>(window);
    // Setup Platform/Renderer backends
    if(!ImGui_ImplGlfw_InitForOpenGL(gWindow, true))
    {
        py::print("Cannot init GLFW for OpenGL");
        exit(1);
    }
    const char* glsl_version = "#version 130";
    if(!ImGui_ImplOpenGL3_Init(glsl_version))
    {
        py::print("Cannot init OpenGL");
        exit(1);
    }
}

void shutdownGLFW(void* window)
{
    glfwDestroyWindow(static_cast<GLFWwindow*>(window));
    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    glfwTerminate();
}

void NewFrame()
{
    glfwPollEvents();
    ImGui_ImplOpenGL3_NewFrame();
    ImGui_ImplGlfw_NewFrame();
}

void Render(void* window, const ImVec4& clear_color)
{
    GLFWwindow* gWindow = static_cast<GLFWwindow*>(window);
    int display_w, display_h;
    glfwGetFramebufferSize(gWindow, &display_w, &display_h);
    glViewport(0, 0, display_w, display_h);
    glClearColor(
        clear_color.x * clear_color.w,
        clear_color.y * clear_color.w,
        clear_color.z * clear_color.w,
        clear_color.w
    );
    glClear(GL_COLOR_BUFFER_BIT);
    ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

    glfwSwapBuffers(gWindow);
}

bool ShouldClose(void* window)
{
    return glfwWindowShouldClose(static_cast<GLFWwindow*>(window));
}

void init_backend_glfw(py::module& m)
{
    m.def(
        "Init",
        initGLFW,
        "title"_a,
        "window_width"_a = 0,
        "window_height"_a = 0,
        "swap_interval"_a = 1,
        py::return_value_policy::reference
    );
    m.def("InitContextForGLFW", initContextForGLFW, "window"_a);
    m.def("Shutdown", shutdownGLFW, "window"_a);
    m.def("NewFrame", NewFrame);
    m.def("Render", Render, "window"_a, "clear_color"_a);
    m.def("ShouldClose", ShouldClose, "window"_a);

    /*
    m.def(
        "InitForOpenGL",
        [](void* window, bool install_callbacks)
        {
            ImGui_ImplGlfw_InitForOpenGL(
                static_cast<GLFWwindow*>(window),
                install_callbacks
            );
        },
        "window"_a,
        "install_callbacks"_a
    );
    m.def(
        "InitForVulkan",
        [](void* window, bool install_callbacks)
        {
            ImGui_ImplGlfw_InitForVulkan(
                static_cast<GLFWwindow*>(window),
                install_callbacks
            );
        },
        "window"_a,
        "install_callbacks"_a
    );
    m.def(
        "InitForOther",
        [](void* window, bool install_callbacks)
        {
            ImGui_ImplGlfw_InitForOther(
                static_cast<GLFWwindow*>(window),
                install_callbacks
            );
        },
        "window"_a,
        "install_callbacks"_a
    );
    m.def("Shutdown", ImGui_ImplGlfw_Shutdown);
    m.def("NewFrame", ImGui_ImplGlfw_NewFrame);
    m.def(
        "InstallCallbacks",
        [](void* window)
        {
            ImGui_ImplGlfw_InstallCallbacks(static_cast<GLFWwindow*>(window));
        },
        "window"_a
    );
    m.def(
        "RestoreCallbacks",
        [](void* window)
        {
            ImGui_ImplGlfw_RestoreCallbacks(static_cast<GLFWwindow*>(window));
        },
        "window"_a
    );
    m.def(
        "WindowFocusCallback",
        [](void* window, int focused)
        {
            ImGui_ImplGlfw_WindowFocusCallback(
                static_cast<GLFWwindow*>(window),
                focused
            );
        },
        "window"_a,
        "focused"_a
    );
    m.def(
        "CursorEnterCallback",
        [](void* window, int entered)
        {
            ImGui_ImplGlfw_CursorEnterCallback(
                static_cast<GLFWwindow*>(window),
                entered
            );
        },
        "window"_a,
        "entered"_a
    );
    m.def(
        "CursorPosCallback",
        [](void* window, double x, double y)
        {
            ImGui_ImplGlfw_CursorPosCallback(
                static_cast<GLFWwindow*>(window),
                x,
                y
            );
        },
        "window"_a,
        "x"_a,
        "y"_a
    );
    m.def(
        "MouseButtonCallback",
        [](void* window, int button, int action, int mods)
        {
            ImGui_ImplGlfw_MouseButtonCallback(
                static_cast<GLFWwindow*>(window),
                button,
                action,
                mods
            );
        },
        "window"_a,
        "button"_a,
        "action"_a,
        "mods"_a
    );
    m.def(
        "ScrollCallback",
        [](void* window, double xoffset, double yoffset)
        {
            ImGui_ImplGlfw_ScrollCallback(
                static_cast<GLFWwindow*>(window),
                xoffset,
                yoffset
            );
        },
        "window"_a,
        "xoffset"_a,
        "yoffset"_a
    );
    m.def(
        "KeyCallback",
        [](void* window, int key, int scancode, int action, int mods)
        {
            ImGui_ImplGlfw_KeyCallback(
                static_cast<GLFWwindow*>(window),
                key,
                scancode,
                action,
                mods
            );
        },
        "window"_a,
        "key"_a,
        "scancode"_a,
        "action"_a,
        "mods"_a
    );
    m.def(
        "CharCallback",
        [](void* window, unsigned int c)
        {
            ImGui_ImplGlfw_CharCallback(static_cast<GLFWwindow*>(window), c);
        },
        "window"_a,
        "c"_a
    );
    m.def(
        "MonitorCallback",
        [](void* window, int event)
        {
            ImGui_ImplGlfw_MonitorCallback(
                static_cast<GLFWmonitor*>(window),
                event
            );
        },
        "window"_a,
        "event"_a
    );
    */
}
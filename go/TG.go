package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
)

// copyFile copies a file from src to dst. If dst exists, it will be replaced.
func copyFile(src, dst string) error {
	sourceFileStat, err := os.Stat(src)
	if err != nil {
		return err
	}

	if !sourceFileStat.Mode().IsRegular() {
		return fmt.Errorf("%s is not a regular file", src)
	}

	source, err := os.Open(src)
	if err != nil {
		return err
	}
	defer source.Close()

	destination, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer destination.Close()

	_, err = io.Copy(destination, source)
	if err != nil {
		return err
	}

	return nil
}

// copyDir copies a whole directory recursively from src to dst.
func copyDir(src string, dst string) error {
	var err error
	var fds []os.DirEntry
	if fds, err = os.ReadDir(src); err != nil {
		return err
	}

	for _, fd := range fds {
		srcPath := filepath.Join(src, fd.Name())
		dstPath := filepath.Join(dst, fd.Name())

		if fd.IsDir() {
			if err = os.MkdirAll(dstPath, os.ModePerm); err != nil {
				return err
			}
			if err = copyDir(srcPath, dstPath); err != nil {
				return err
			}
		} else {
			if err = copyFile(srcPath, dstPath); err != nil {
				return err
			}
		}
	}
	return nil
}

// 如果有更新文件夹, 里面会有一个文件包含所有远程文件名的 all_remote_file.txt, 用 \n 隔开
func loadRemoteFileList(filePath string) (map[string]struct{}, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	remoteFiles := make(map[string]struct{})
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" {
			remoteFiles[line] = struct{}{}
		}
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return remoteFiles, nil
}

// removeUnlistedFiles traverses main.dist and removes files not listed in remoteFiles.
func removeUnlistedFiles(dir string, remoteFiles map[string]struct{}) error {
	return filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		// Get the relative path
		relPath, err := filepath.Rel(dir, path)
		if err != nil {
			return err
		}

		// Convert path to Unix-style for consistency with all_remote_file.txt format
		relPath = filepath.ToSlash(relPath)

		// If the file is not in the remote file list, delete it
		if _, exists := remoteFiles[relPath]; !exists && !info.IsDir() {
			fmt.Printf("Removing unlisted file: %s\n", path)
			if err := os.Remove(path); err != nil {
				return err
			}
		}

		return nil
	})
}

// 应用更新并删除更新文件夹
func updateFile(updateDir string, allRemoteFile string, mainDistDir string) error {

	remoteFileListPath := filepath.Join(updateDir, allRemoteFile)
	remoteFiles, err := loadRemoteFileList(remoteFileListPath)
	if err != nil {
		return fmt.Errorf("failed to load remote file list: %v", err)
	}

	// Remove unlisted files in main.dist
	err = removeUnlistedFiles(mainDistDir, remoteFiles)
	if err != nil {
		return fmt.Errorf("failed to remove unlisted files: %v", err)
	}

	// Copy the files from .temp_update to main.dist
	err = copyDir(updateDir, mainDistDir)
	if err != nil {
		return fmt.Errorf("failed to update files: %v", err)
	}

	// Delete the .temp_update directory after successful update
	err = os.RemoveAll(updateDir)
	if err != nil {
		return fmt.Errorf("failed to remove .temp_update directory: %v", err)
	}

	fmt.Println("Update completed successfully.")
	return nil
}

// 运行主文件
func launchMainApp(mainAppPath string) error {
	// Execute the main application
	fmt.Printf("Launching the main application: %s\n", mainAppPath)
	err, _ := os.StartProcess(
		mainAppPath,
		[]string{"--run", "--webEngineArgs", "--remote-debugging-port=22234", "--remote-allow-origins=*"},
		&os.ProcAttr{
			Files: []*os.File{os.Stdin, os.Stdout, os.Stderr},
		},
	)
	if err != nil {
		return fmt.Errorf("failed to launch main application: %v", err)
	}

	return nil
}

func main() {
	// Directories
	updateDir := "./data/temp_update"
	allRemoteFile := "all_remote_file.txt"

	mainDistDir := "./main.dist"
	mainAppName := "main.exe"

	mainAppPath := filepath.Join(mainDistDir, mainAppName)

	if _, err := os.Stat(updateDir); os.IsNotExist(err) {
		fmt.Println("update dir not found.")
	} else {
		err := updateFile(updateDir, allRemoteFile, mainDistDir)
		if err != nil {
			fmt.Printf("Error during update: %v\n", err)
			return
		}
	}

	err := launchMainApp(mainAppPath)
	if err != nil {
		fmt.Printf("Error launching main application: %v\n", err)
	}
}

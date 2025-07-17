package com.tiktubstudio.ui.panels;

import com.tiktubstudio.api.ApiClient;
import com.tiktubstudio.ui.MainWindow;

import javax.swing.*;
import java.awt.*;
import java.io.File;

/**
 * Panel untuk upload video
 */
public class UploadPanel extends JPanel {
    private ApiClient apiClient;
    private MainWindow mainWindow;
    private JButton chooseFileButton;
    private JLabel fileInfoLabel;
    private File selectedFile;
    
    public UploadPanel(ApiClient apiClient, MainWindow mainWindow) {
        this.apiClient = apiClient;
        this.mainWindow = mainWindow;
        initializeComponents();
        setupUI();
    }
    
    private void initializeComponents() {
        chooseFileButton = new JButton("📁 Choose Video File");
        fileInfoLabel = new JLabel("No file selected");
    }
    
    private void setupUI() {
        setLayout(new BorderLayout());
        setBackground(new Color(32, 32, 35));
        
        // Create main content panel
        JPanel contentPanel = new JPanel(new GridBagLayout());
        contentPanel.setBackground(new Color(32, 32, 35));
        contentPanel.setBorder(BorderFactory.createEmptyBorder(50, 50, 50, 50));
        
        GridBagConstraints gbc = new GridBagConstraints();
        
        // Upload icon
        JLabel uploadIcon = new JLabel("🎬", JLabel.CENTER);
        uploadIcon.setFont(new Font("Arial", Font.PLAIN, 72));
        gbc.gridx = 0; gbc.gridy = 0; gbc.insets = new Insets(0, 0, 20, 0);
        contentPanel.add(uploadIcon, gbc);
        
        // Title
        JLabel titleLabel = new JLabel("Upload Your Video", JLabel.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 24));
        titleLabel.setForeground(Color.WHITE);
        gbc.gridy = 1; gbc.insets = new Insets(0, 0, 10, 0);
        contentPanel.add(titleLabel, gbc);
        
        // Description
        JLabel descLabel = new JLabel("<html><center>Select a video file to transform into engaging short clips<br>Supported formats: MP4, MOV, AVI, MKV</center></html>", JLabel.CENTER);
        descLabel.setFont(new Font("Arial", Font.PLAIN, 14));
        descLabel.setForeground(new Color(180, 180, 180));
        gbc.gridy = 2; gbc.insets = new Insets(0, 0, 30, 0);
        contentPanel.add(descLabel, gbc);
        
        // Choose file button
        chooseFileButton.setFont(new Font("Arial", Font.BOLD, 16));
        chooseFileButton.setBackground(new Color(255, 0, 80));
        chooseFileButton.setForeground(Color.WHITE);
        chooseFileButton.setFocusPainted(false);
        chooseFileButton.setBorder(BorderFactory.createEmptyBorder(15, 30, 15, 30));
        chooseFileButton.setCursor(new Cursor(Cursor.HAND_CURSOR));
        chooseFileButton.addActionListener(e -> chooseFile());
        gbc.gridy = 3; gbc.insets = new Insets(0, 0, 20, 0);
        contentPanel.add(chooseFileButton, gbc);
        
        // File info
        fileInfoLabel.setFont(new Font("Arial", Font.PLAIN, 12));
        fileInfoLabel.setForeground(new Color(160, 160, 160));
        gbc.gridy = 4; gbc.insets = new Insets(0, 0, 0, 0);
        contentPanel.add(fileInfoLabel, gbc);
        
        add(contentPanel, BorderLayout.CENTER);
    }
    
    private void chooseFile() {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setFileFilter(new javax.swing.filechooser.FileNameExtensionFilter(
            "Video Files", "mp4", "mov", "avi", "mkv", "webm", "flv"));
        
        int result = fileChooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            selectedFile = fileChooser.getSelectedFile();
            updateFileInfo();
            mainWindow.switchToProcessingTab();
        }
    }
    
    private void updateFileInfo() {
        if (selectedFile != null) {
            long fileSize = selectedFile.length();
            String sizeStr = formatFileSize(fileSize);
            fileInfoLabel.setText("Selected: " + selectedFile.getName() + " (" + sizeStr + ")");
        }
    }
    
    private String formatFileSize(long bytes) {
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1024 * 1024) return String.format("%.1f KB", bytes / 1024.0);
        if (bytes < 1024 * 1024 * 1024) return String.format("%.1f MB", bytes / (1024.0 * 1024));
        return String.format("%.1f GB", bytes / (1024.0 * 1024 * 1024));
    }
    
    public File getSelectedFile() {
        return selectedFile;
    }
}
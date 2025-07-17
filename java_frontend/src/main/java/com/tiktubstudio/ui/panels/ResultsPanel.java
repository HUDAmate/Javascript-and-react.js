package com.tiktubstudio.ui.panels;

import com.tiktubstudio.api.ApiClient;
import com.tiktubstudio.ui.MainWindow;

import javax.swing.*;
import java.awt.*;

/**
 * Panel untuk menampilkan dan download hasil video
 */
public class ResultsPanel extends JPanel {
    private ApiClient apiClient;
    private MainWindow mainWindow;
    
    public ResultsPanel(ApiClient apiClient, MainWindow mainWindow) {
        this.apiClient = apiClient;
        this.mainWindow = mainWindow;
        initializeComponents();
        setupUI();
    }
    
    private void initializeComponents() {
        // Components will be initialized here
    }
    
    private void setupUI() {
        setLayout(new BorderLayout());
        setBackground(new Color(32, 32, 35));
        
        // Create main content panel
        JPanel contentPanel = new JPanel(new GridBagLayout());
        contentPanel.setBackground(new Color(32, 32, 35));
        contentPanel.setBorder(BorderFactory.createEmptyBorder(50, 50, 50, 50));
        
        GridBagConstraints gbc = new GridBagConstraints();
        
        // Results icon
        JLabel resultsIcon = new JLabel("🎉", JLabel.CENTER);
        resultsIcon.setFont(new Font("Arial", Font.PLAIN, 72));
        gbc.gridx = 0; gbc.gridy = 0; gbc.insets = new Insets(0, 0, 20, 0);
        contentPanel.add(resultsIcon, gbc);
        
        // Title
        JLabel titleLabel = new JLabel("Processing Complete!", JLabel.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 24));
        titleLabel.setForeground(Color.WHITE);
        gbc.gridy = 1; gbc.insets = new Insets(0, 0, 10, 0);
        contentPanel.add(titleLabel, gbc);
        
        // Description
        JLabel descLabel = new JLabel("<html><center>Your short videos are ready for download<br>Click the buttons below to preview or download</center></html>", JLabel.CENTER);
        descLabel.setFont(new Font("Arial", Font.PLAIN, 14));
        descLabel.setForeground(new Color(180, 180, 180));
        gbc.gridy = 2; gbc.insets = new Insets(0, 0, 30, 0);
        contentPanel.add(descLabel, gbc);
        
        // Sample video buttons
        JPanel videoPanel = new JPanel(new FlowLayout());
        videoPanel.setBackground(new Color(32, 32, 35));
        
        for (int i = 1; i <= 3; i++) {
            JButton videoButton = new JButton("📱 Video " + i + " (Energetic)");
            styleVideoButton(videoButton);
            videoPanel.add(videoButton);
        }
        
        gbc.gridy = 3; gbc.insets = new Insets(0, 0, 20, 0);
        contentPanel.add(videoPanel, gbc);
        
        // Download all button
        JButton downloadAllButton = new JButton("💾 Download All Videos");
        styleDownloadButton(downloadAllButton);
        gbc.gridy = 4; gbc.insets = new Insets(0, 0, 0, 0);
        contentPanel.add(downloadAllButton, gbc);
        
        add(contentPanel, BorderLayout.CENTER);
    }
    
    private void styleVideoButton(JButton button) {
        button.setBackground(new Color(45, 45, 48));
        button.setForeground(Color.WHITE);
        button.setFont(new Font("Arial", Font.PLAIN, 12));
        button.setFocusPainted(false);
        button.setBorder(BorderFactory.createEmptyBorder(10, 15, 10, 15));
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));
        button.setPreferredSize(new Dimension(180, 40));
        
        // Hover effect
        button.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseEntered(java.awt.event.MouseEvent evt) {
                button.setBackground(new Color(60, 60, 65));
            }
            public void mouseExited(java.awt.event.MouseEvent evt) {
                button.setBackground(new Color(45, 45, 48));
            }
        });
    }
    
    private void styleDownloadButton(JButton button) {
        button.setBackground(new Color(255, 0, 80));
        button.setForeground(Color.WHITE);
        button.setFont(new Font("Arial", Font.BOLD, 14));
        button.setFocusPainted(false);
        button.setBorder(BorderFactory.createEmptyBorder(12, 25, 12, 25));
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));
        
        // Hover effect
        button.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseEntered(java.awt.event.MouseEvent evt) {
                button.setBackground(new Color(230, 0, 70));
            }
            public void mouseExited(java.awt.event.MouseEvent evt) {
                button.setBackground(new Color(255, 0, 80));
            }
        });
    }
}
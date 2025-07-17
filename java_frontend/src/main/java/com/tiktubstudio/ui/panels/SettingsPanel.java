package com.tiktubstudio.ui.panels;

import com.tiktubstudio.ui.MainWindow;

import javax.swing.*;
import java.awt.*;

/**
 * Panel untuk pengaturan aplikasi
 */
public class SettingsPanel extends JPanel {
    private MainWindow mainWindow;
    
    public SettingsPanel(MainWindow mainWindow) {
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
        
        // Settings icon
        JLabel settingsIcon = new JLabel("⚙️", JLabel.CENTER);
        settingsIcon.setFont(new Font("Arial", Font.PLAIN, 72));
        gbc.gridx = 0; gbc.gridy = 0; gbc.insets = new Insets(0, 0, 20, 0);
        contentPanel.add(settingsIcon, gbc);
        
        // Title
        JLabel titleLabel = new JLabel("Application Settings", JLabel.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 24));
        titleLabel.setForeground(Color.WHITE);
        gbc.gridy = 1; gbc.insets = new Insets(0, 0, 10, 0);
        contentPanel.add(titleLabel, gbc);
        
        // Description
        JLabel descLabel = new JLabel("<html><center>Configure TikTub Studio preferences<br>Settings will be saved automatically</center></html>", JLabel.CENTER);
        descLabel.setFont(new Font("Arial", Font.PLAIN, 14));
        descLabel.setForeground(new Color(180, 180, 180));
        gbc.gridy = 2; gbc.insets = new Insets(0, 0, 30, 0);
        contentPanel.add(descLabel, gbc);
        
        // Settings form
        JPanel settingsForm = createSettingsForm();
        gbc.gridy = 3; gbc.insets = new Insets(0, 0, 0, 0);
        contentPanel.add(settingsForm, gbc);
        
        add(contentPanel, BorderLayout.CENTER);
    }
    
    private JPanel createSettingsForm() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setBackground(new Color(32, 32, 35));
        panel.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createLineBorder(new Color(255, 0, 80)), 
            "Preferences", 
            0, 0, 
            new Font("Arial", Font.BOLD, 14), 
            Color.WHITE
        ));
        
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(10, 10, 10, 10);
        gbc.anchor = GridBagConstraints.WEST;
        
        // Output directory
        gbc.gridx = 0; gbc.gridy = 0;
        panel.add(createLabel("Output Directory:"), gbc);
        gbc.gridx = 1;
        JTextField outputDirField = new JTextField("/path/to/output");
        styleTextField(outputDirField);
        panel.add(outputDirField, gbc);
        
        // Video quality
        gbc.gridx = 0; gbc.gridy = 1;
        panel.add(createLabel("Video Quality:"), gbc);
        gbc.gridx = 1;
        JComboBox<String> qualityCombo = new JComboBox<>(new String[]{"High", "Medium", "Low"});
        styleComboBox(qualityCombo);
        panel.add(qualityCombo, gbc);
        
        // Auto-effects
        gbc.gridx = 0; gbc.gridy = 2;
        panel.add(createLabel("Auto Effects:"), gbc);
        gbc.gridx = 1;
        JCheckBox autoEffectsCheck = new JCheckBox("Enable automatic effects", true);
        styleCheckBox(autoEffectsCheck);
        panel.add(autoEffectsCheck, gbc);
        
        // Auto-preview
        gbc.gridx = 0; gbc.gridy = 3;
        panel.add(createLabel("Auto Preview:"), gbc);
        gbc.gridx = 1;
        JCheckBox autoPreviewCheck = new JCheckBox("Enable automatic preview", true);
        styleCheckBox(autoPreviewCheck);
        panel.add(autoPreviewCheck, gbc);
        
        return panel;
    }
    
    private JLabel createLabel(String text) {
        JLabel label = new JLabel(text);
        label.setForeground(Color.WHITE);
        label.setFont(new Font("Arial", Font.PLAIN, 12));
        label.setPreferredSize(new Dimension(120, 25));
        return label;
    }
    
    private void styleTextField(JTextField field) {
        field.setBackground(new Color(45, 45, 48));
        field.setForeground(Color.WHITE);
        field.setFont(new Font("Arial", Font.PLAIN, 12));
        field.setBorder(BorderFactory.createEmptyBorder(5, 8, 5, 8));
        field.setPreferredSize(new Dimension(200, 30));
    }
    
    private void styleComboBox(JComboBox<String> combo) {
        combo.setBackground(new Color(45, 45, 48));
        combo.setForeground(Color.WHITE);
        combo.setFont(new Font("Arial", Font.PLAIN, 12));
        combo.setFocusable(false);
        combo.setPreferredSize(new Dimension(200, 30));
    }
    
    private void styleCheckBox(JCheckBox checkBox) {
        checkBox.setBackground(new Color(32, 32, 35));
        checkBox.setForeground(Color.WHITE);
        checkBox.setFont(new Font("Arial", Font.PLAIN, 12));
        checkBox.setFocusPainted(false);
    }
}
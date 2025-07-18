package com.tiktubstudio.ui.panels;

import com.tiktubstudio.ui.components.ModernButton;
import com.tiktubstudio.ui.components.RoundedPanel;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.*;
import java.awt.datatransfer.DataFlavor;
import java.awt.datatransfer.Transferable;
import java.awt.dnd.*;
import java.awt.event.ActionEvent;
import java.io.File;
import java.util.List;
import java.util.function.Consumer;

/**
 * Modern video upload card dengan drag-and-drop support
 */
public class VideoUploadCard extends RoundedPanel {
    
    private Consumer<File> fileSelectedCallback;
    private JPanel uploadArea;
    private JPanel fileInfoPanel;
    private File selectedFile;
    
    // UI Colors
    private static final Color PRIMARY_GREEN = new Color(88, 204, 2);
    private static final Color BACKGROUND_LIGHT = new Color(248, 250, 252);
    private static final Color CARD_BACKGROUND = new Color(255, 255, 255);
    private static final Color TEXT_PRIMARY = new Color(59, 72, 80);
    private static final Color TEXT_SECONDARY = new Color(119, 137, 151);
    private static final Color BORDER_COLOR = new Color(229, 232, 235);
    private static final Color SUCCESS_GREEN = new Color(46, 213, 115);
    private static final Color UPLOAD_HOVER = new Color(PRIMARY_GREEN.getRed(), PRIMARY_GREEN.getGreen(), PRIMARY_GREEN.getBlue(), 30);
    
    public VideoUploadCard() {
        super(16, CARD_BACKGROUND, true);
        initializeCard();
        setupDropTarget();
    }
    
    private void initializeCard() {
        setLayout(new BorderLayout());
        setBorder(new EmptyBorder(40, 40, 40, 40));
        setPreferredSize(new Dimension(600, 400));
        
        createUploadArea();
        createFileInfoPanel();
        
        // Initially show upload area
        add(uploadArea, BorderLayout.CENTER);
    }
    
    private void createUploadArea() {
        uploadArea = new JPanel();
        uploadArea.setLayout(new BoxLayout(uploadArea, BoxLayout.Y_AXIS));
        uploadArea.setOpaque(false);
        
        // Upload icon
        JLabel iconLabel = new JLabel("📁");
        iconLabel.setFont(new Font("Segoe UI Emoji", Font.PLAIN, 64));
        iconLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        // Main title
        JLabel titleLabel = new JLabel("Drop your video here");
        titleLabel.setFont(new Font("Segoe UI", Font.BOLD, 24));
        titleLabel.setForeground(TEXT_PRIMARY);
        titleLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        // Subtitle
        JLabel subtitleLabel = new JLabel("or click to browse files");
        subtitleLabel.setFont(new Font("Segoe UI", Font.PLAIN, 16));
        subtitleLabel.setForeground(TEXT_SECONDARY);
        subtitleLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        // Format info
        JLabel formatLabel = new JLabel("Supports MP4, MOV, AVI, MKV (max 2GB)");
        formatLabel.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        formatLabel.setForeground(TEXT_SECONDARY);
        formatLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        // Browse button
        ModernButton browseButton = new ModernButton("Choose Video File", ModernButton.ButtonStyle.OUTLINE);
        browseButton.setIcon("🔍");
        browseButton.setAlignmentX(Component.CENTER_ALIGNMENT);
        browseButton.addActionListener(this::onBrowseButtonClicked);
        
        // Add components with spacing
        uploadArea.add(Box.createVerticalGlue());
        uploadArea.add(iconLabel);
        uploadArea.add(Box.createVerticalStrut(20));
        uploadArea.add(titleLabel);
        uploadArea.add(Box.createVerticalStrut(8));
        uploadArea.add(subtitleLabel);
        uploadArea.add(Box.createVerticalStrut(30));
        uploadArea.add(browseButton);
        uploadArea.add(Box.createVerticalStrut(20));
        uploadArea.add(formatLabel);
        uploadArea.add(Box.createVerticalGlue());
        
        // Make entire area clickable
        uploadArea.addMouseListener(new java.awt.event.MouseAdapter() {
            @Override
            public void mouseClicked(java.awt.event.MouseEvent e) {
                onBrowseButtonClicked(null);
            }
        });
        
        // Add hover effect
        uploadArea.addMouseListener(new java.awt.event.MouseAdapter() {
            @Override
            public void mouseEntered(java.awt.event.MouseEvent e) {
                setBackground(UPLOAD_HOVER);
            }
            
            @Override
            public void mouseExited(java.awt.event.MouseEvent e) {
                setBackground(CARD_BACKGROUND);
            }
        });
    }
    
    private void createFileInfoPanel() {
        fileInfoPanel = new JPanel(new BorderLayout());
        fileInfoPanel.setOpaque(false);
        fileInfoPanel.setBorder(new EmptyBorder(20, 20, 20, 20));
        
        // Success panel
        JPanel successPanel = new JPanel();
        successPanel.setLayout(new BoxLayout(successPanel, BoxLayout.Y_AXIS));
        successPanel.setOpaque(false);
        
        // Success icon and message
        JLabel successIcon = new JLabel("✅");
        successIcon.setFont(new Font("Segoe UI Emoji", Font.PLAIN, 48));
        successIcon.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        JLabel successTitle = new JLabel("Video Selected Successfully!");
        successTitle.setFont(new Font("Segoe UI", Font.BOLD, 20));
        successTitle.setForeground(SUCCESS_GREEN);
        successTitle.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        successPanel.add(Box.createVerticalStrut(20));
        successPanel.add(successIcon);
        successPanel.add(Box.createVerticalStrut(16));
        successPanel.add(successTitle);
        successPanel.add(Box.createVerticalStrut(30));
        
        // File details panel
        JPanel detailsPanel = createFileDetailsPanel();
        
        // Action buttons
        JPanel buttonsPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 20, 0));
        buttonsPanel.setOpaque(false);
        
        ModernButton changeButton = new ModernButton("Change Video", ModernButton.ButtonStyle.OUTLINE);
        changeButton.setIcon("🔄");
        changeButton.addActionListener(this::onChangeVideoClicked);
        
        ModernButton previewButton = new ModernButton("Preview Video", ModernButton.ButtonStyle.SECONDARY);
        previewButton.setIcon("👁️");
        previewButton.addActionListener(this::onPreviewClicked);
        
        buttonsPanel.add(changeButton);
        buttonsPanel.add(previewButton);
        
        fileInfoPanel.add(successPanel, BorderLayout.NORTH);
        fileInfoPanel.add(detailsPanel, BorderLayout.CENTER);
        fileInfoPanel.add(buttonsPanel, BorderLayout.SOUTH);
    }
    
    private JPanel createFileDetailsPanel() {
        JPanel panel = new RoundedPanel(8);
        panel.setBackground(BACKGROUND_LIGHT);
        panel.setBorder(new EmptyBorder(20, 24, 20, 24));
        panel.setLayout(new GridBagLayout());
        
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.anchor = GridBagConstraints.WEST;
        gbc.insets = new Insets(4, 0, 4, 20);
        
        // File details will be populated when file is selected
        
        return panel;
    }
    
    private void populateFileDetails(File file, JPanel detailsPanel) {
        detailsPanel.removeAll();
        
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.anchor = GridBagConstraints.WEST;
        gbc.insets = new Insets(4, 0, 4, 20);
        
        // File name
        addDetailRow(detailsPanel, gbc, 0, "📄", "File Name:", file.getName());
        
        // File size
        String fileSize = formatFileSize(file.length());
        addDetailRow(detailsPanel, gbc, 1, "💾", "File Size:", fileSize);
        
        // File path
        String path = file.getAbsolutePath();
        if (path.length() > 50) {
            path = "..." + path.substring(path.length() - 47);
        }
        addDetailRow(detailsPanel, gbc, 2, "📁", "Location:", path);
        
        // Format (from extension)
        String extension = getFileExtension(file).toUpperCase();
        addDetailRow(detailsPanel, gbc, 3, "🎬", "Format:", extension);
        
        detailsPanel.revalidate();
        detailsPanel.repaint();
    }
    
    private void addDetailRow(JPanel panel, GridBagConstraints gbc, int row, String icon, String label, String value) {
        gbc.gridy = row;
        
        // Icon
        gbc.gridx = 0;
        JLabel iconLabel = new JLabel(icon);
        iconLabel.setFont(new Font("Segoe UI Emoji", Font.PLAIN, 16));
        panel.add(iconLabel, gbc);
        
        // Label
        gbc.gridx = 1;
        JLabel labelComponent = new JLabel(label);
        labelComponent.setFont(new Font("Segoe UI", Font.BOLD, 13));
        labelComponent.setForeground(TEXT_PRIMARY);
        panel.add(labelComponent, gbc);
        
        // Value
        gbc.gridx = 2;
        gbc.weightx = 1.0;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        JLabel valueComponent = new JLabel(value);
        valueComponent.setFont(new Font("Segoe UI", Font.PLAIN, 13));
        valueComponent.setForeground(TEXT_SECONDARY);
        panel.add(valueComponent, gbc);
        
        gbc.weightx = 0.0;
        gbc.fill = GridBagConstraints.NONE;
    }
    
    private void setupDropTarget() {
        setDropTarget(new DropTarget() {
            @Override
            public synchronized void drop(DropTargetDropEvent evt) {
                try {
                    evt.acceptDrop(DnDConstants.ACTION_COPY);
                    
                    Transferable transferable = evt.getTransferable();
                    if (transferable.isDataFlavorSupported(DataFlavor.javaFileListFlavor)) {
                        @SuppressWarnings("unchecked")
                        List<File> droppedFiles = (List<File>) transferable.getTransferData(DataFlavor.javaFileListFlavor);
                        
                        if (!droppedFiles.isEmpty()) {
                            File file = droppedFiles.get(0);
                            if (isValidVideoFile(file)) {
                                handleFileSelection(file);
                            } else {
                                showErrorMessage("Invalid file format. Please select a video file (MP4, MOV, AVI, MKV).");
                            }
                        }
                    }
                    
                    evt.dropComplete(true);
                } catch (Exception e) {
                    e.printStackTrace();
                    evt.dropComplete(false);
                }
            }
            
            @Override
            public synchronized void dragOver(DropTargetDragEvent dtde) {
                if (isDragAcceptable(dtde)) {
                    setBackground(UPLOAD_HOVER);
                    dtde.acceptDrag(DnDConstants.ACTION_COPY);
                } else {
                    dtde.rejectDrag();
                }
            }
            
            @Override
            public synchronized void dragExit(DropTargetEvent dte) {
                setBackground(CARD_BACKGROUND);
            }
            
            private boolean isDragAcceptable(DropTargetDragEvent dtde) {
                return dtde.getTransferable().isDataFlavorSupported(DataFlavor.javaFileListFlavor);
            }
        });
    }
    
    private void onBrowseButtonClicked(ActionEvent e) {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Select Video File");
        fileChooser.setFileFilter(new FileNameExtensionFilter(
            "Video Files (*.mp4, *.mov, *.avi, *.mkv)", 
            "mp4", "mov", "avi", "mkv"
        ));
        
        int result = fileChooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            if (isValidVideoFile(selectedFile)) {
                handleFileSelection(selectedFile);
            } else {
                showErrorMessage("Invalid file format or size. Please select a video file under 2GB.");
            }
        }
    }
    
    private void onChangeVideoClicked(ActionEvent e) {
        // Switch back to upload view
        removeAll();
        add(uploadArea, BorderLayout.CENTER);
        selectedFile = null;
        revalidate();
        repaint();
    }
    
    private void onPreviewClicked(ActionEvent e) {
        if (selectedFile != null) {
            // Open simple preview dialog
            showVideoPreview(selectedFile);
        }
    }
    
    private void handleFileSelection(File file) {
        this.selectedFile = file;
        
        // Update file details
        populateFileDetails(file, (JPanel) ((JPanel) fileInfoPanel.getComponent(1)));
        
        // Switch to file info view
        removeAll();
        add(fileInfoPanel, BorderLayout.CENTER);
        revalidate();
        repaint();
        
        // Notify callback
        if (fileSelectedCallback != null) {
            fileSelectedCallback.accept(file);
        }
    }
    
    public void showSelectedFile(File file) {
        this.selectedFile = file;
        populateFileDetails(file, (JPanel) ((JPanel) fileInfoPanel.getComponent(1)));
    }
    
    private boolean isValidVideoFile(File file) {
        if (file == null || !file.exists() || !file.isFile()) {
            return false;
        }
        
        // Check file size (max 2GB)
        if (file.length() > 2L * 1024 * 1024 * 1024) {
            return false;
        }
        
        // Check file extension
        String extension = getFileExtension(file).toLowerCase();
        return extension.equals("mp4") || extension.equals("mov") || 
               extension.equals("avi") || extension.equals("mkv");
    }
    
    private String getFileExtension(File file) {
        String name = file.getName();
        int lastDot = name.lastIndexOf('.');
        return lastDot > 0 ? name.substring(lastDot + 1) : "";
    }
    
    private String formatFileSize(long bytes) {
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1024 * 1024) return String.format("%.1f KB", bytes / 1024.0);
        if (bytes < 1024 * 1024 * 1024) return String.format("%.1f MB", bytes / (1024.0 * 1024));
        return String.format("%.1f GB", bytes / (1024.0 * 1024 * 1024));
    }
    
    private void showErrorMessage(String message) {
        JOptionPane.showMessageDialog(this, message, "Error", JOptionPane.ERROR_MESSAGE);
    }
    
    private void showVideoPreview(File file) {
        JDialog previewDialog = new JDialog((Frame) SwingUtilities.getWindowAncestor(this), "Video Preview", true);
        previewDialog.setSize(400, 300);
        previewDialog.setLocationRelativeTo(this);
        
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBorder(new EmptyBorder(20, 20, 20, 20));
        
        JLabel infoLabel = new JLabel("<html><center><h3>Video Preview</h3><br>" +
            "File: " + file.getName() + "<br>" +
            "Size: " + formatFileSize(file.length()) + "<br><br>" +
            "Full video preview will be available<br>after processing starts.</center></html>");
        infoLabel.setHorizontalAlignment(SwingConstants.CENTER);
        
        ModernButton closeButton = new ModernButton("Close", ModernButton.ButtonStyle.PRIMARY);
        closeButton.addActionListener(e -> previewDialog.dispose());
        
        JPanel buttonPanel = new JPanel(new FlowLayout());
        buttonPanel.add(closeButton);
        
        panel.add(infoLabel, BorderLayout.CENTER);
        panel.add(buttonPanel, BorderLayout.SOUTH);
        
        previewDialog.add(panel);
        previewDialog.setVisible(true);
    }
    
    public void setFileSelectedCallback(Consumer<File> callback) {
        this.fileSelectedCallback = callback;
    }
    
    public File getSelectedFile() {
        return selectedFile;
    }
}
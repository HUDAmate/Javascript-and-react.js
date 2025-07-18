
import javax.swing.*;
import java.awt.*;

public class QuickDemo {
    public static void main(String[] args) {
        JFrame f = new JFrame("TikTub Studio - AI Video Creator");
        f.setSize(1000, 700);
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        f.setLocationRelativeTo(null);
        
        JPanel p = new JPanel(new BorderLayout());
        p.setBackground(new Color(248, 250, 252));
        
        JLabel title = new JLabel("<html><center><h1>🎬 TikTub Studio Enhanced</h1><br>" +
            "<h2>AI-Powered Short Video Creator</h2><br><br>" +
            "<b>✨ Key Features:</b><br>" +
            "🤖 Advanced AI scene detection<br>" +
            "🎨 Professional effects & transitions<br>" +
            "📝 Auto subtitles with animations<br>" +
            "📱 Modern Duolingo-inspired UI<br>" +
            "🎯 Smart content optimization<br><br>" +
            "<i>Upload → AI Analysis → Effects → Export</i></center></html>");
        title.setHorizontalAlignment(SwingConstants.CENTER);
        title.setFont(new Font("Segoe UI", Font.PLAIN, 16));
        
        JButton btn = new JButton("🚀 Start Processing");
        btn.setFont(new Font("Segoe UI", Font.BOLD, 16));
        btn.setBackground(new Color(88, 204, 2));
        btn.setForeground(Color.WHITE);
        btn.setPreferredSize(new Dimension(200, 50));
        btn.setFocusPainted(false);
        btn.setBorderPainted(false);
        
        JPanel center = new JPanel(new BorderLayout());
        center.setOpaque(false);
        center.add(title, BorderLayout.CENTER);
        
        JPanel bottom = new JPanel();
        bottom.setOpaque(false);
        bottom.add(btn);
        
        p.add(center, BorderLayout.CENTER);
        p.add(bottom, BorderLayout.SOUTH);
        f.add(p);
        f.setVisible(true);
    }
}
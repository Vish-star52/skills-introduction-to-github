package com.ems.servlet;

import java.io.*;
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.*;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

@WebServlet("/upload")
@MultipartConfig
public class UploadServlet extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html;charset=UTF-8");

        PrintWriter out = response.getWriter();

        try {
            // 📁 File Upload
            Part filePart = request.getPart("resume");
            String fileName = filePart.getSubmittedFileName();

            String uploadPath = getServletContext().getRealPath("") + File.separator + "uploads";

            File uploadDir = new File(uploadPath);
            if (!uploadDir.exists()) uploadDir.mkdir();

            File file = new File(uploadPath + File.separator + fileName);
            filePart.write(file.getAbsolutePath());

            // 📄 Extract PDF text
            PDDocument document = PDDocument.load(file);
            PDFTextStripper stripper = new PDFTextStripper();
            String text = stripper.getText(document);
            document.close();

            String lowerText = text.toLowerCase();

            // 📊 Score Calculation
            int skillCount = 0;

            if (lowerText.contains("java")) skillCount++;
            if (lowerText.contains("python")) skillCount++;
            if (lowerText.contains("sql")) skillCount++;
            if (lowerText.contains("machine learning")) skillCount++;
            if (lowerText.contains("spring")) skillCount++;

            int score = skillCount * 20;

            // 💡 Suggestions
            StringBuilder suggestions = new StringBuilder();

            if (!lowerText.contains("java"))
                suggestions.append("• Add Java skills<br>");

            if (!lowerText.contains("python"))
                suggestions.append("• Add Python skills<br>");

            if (!lowerText.contains("sql"))
                suggestions.append("• Add SQL/database knowledge<br>");

            if (!lowerText.contains("project"))
                suggestions.append("• Mention projects<br>");

            if (!lowerText.contains("machine learning"))
                suggestions.append("• Add Machine Learning/AI skills<br>");

            // 🗄️ DATABASE SAVE
            try {
                Class.forName("com.mysql.cj.jdbc.Driver");

                Connection con = DriverManager.getConnection(
                        "jdbc:mysql://localhost:3306/resume_db",
                        "root",
                        "1234"   // 🔴 CHANGE THIS
                );

                PreparedStatement ps = con.prepareStatement(
                        "INSERT INTO resumes(filename, score, suggestions) VALUES (?, ?, ?)"
                );

                ps.setString(1, fileName);
                ps.setInt(2, score);
                ps.setString(3, suggestions.toString());

                ps.executeUpdate();

                con.close();

            } catch (Exception e) {
                e.printStackTrace();
                out.println("<p style='color:red;'>Database Error!</p>");
            }

            // 🎨 UI Output
            out.println("<html><head><title>Resume Analyzer</title></head><body>");

            out.println("<h2>✅ Resume Uploaded Successfully</h2>");
            out.println("<h3>📄 File: " + fileName + "</h3>");

            out.println("<h3>📊 Resume Score: " + score + "/100</h3>");

            if (score >= 80) {
                out.println("<p style='color:green;'>Excellent Resume 🚀</p>");
            } else if (score >= 50) {
                out.println("<p style='color:orange;'>Good Resume 👍</p>");
            } else {
                out.println("<p style='color:red;'>Needs Improvement ⚠️</p>");
            }

            out.println("<h3>💡 Suggestions:</h3>");

            if (suggestions.length() == 0) {
                out.println("✔ No major suggestions. Great job!");
            } else {
                out.println(suggestions.toString());
            }

            out.println("<h3>📜 Extracted Content:</h3>");
            out.println("<pre style='background:#f4f4f4;padding:10px;border:1px solid #ccc;'>");
            out.println(text);
            out.println("</pre>");

            out.println("</body></html>");

        } catch (Exception e) {
            e.printStackTrace();
            out.println("<h2 style='color:red;'>Error occurred!</h2>");
        }
    }
}
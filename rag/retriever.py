print("🚀 retriever.py ĐANG CHẠY")

from langchain_community.vectorstores import Chroma
from rag.embedding import get_embedding_model
from rag.template import admission_chain

CHROMA_PATH = "chroma_db"

AUTOMATION_STATIC_ANSWER = """
NGÀNH CÔNG NGHỆ KỸ THUẬT ĐIỀU KHIỂN VÀ TỰ ĐỘNG HÓA (7510303V, 7510303A) - (AUN-QA)
KHOA ĐIỆN ĐIỆN TỬ, TRƯỜNG ĐẠI HỌC SƯ PHẠM KỸ THUẬT TP. HỒ CHÍ MINH
1. Giới thiệu về ngành:
Sinh viên học ngành này sẽ được trang bị kiến thức về khoa học cơ bản và chuyên ngành Tự động hóa; có khả năng thiết kế và thi công, vận hành, sửa chữa, nâng cấp các hệ thống sản xuất tự động trong công nghiệp. Sinh viên được đào tạo theo hướng công nghệ tiên tiến; có nhiều thời gian học thực hành trên các hệ thống sản xuất thực tế, hiện đại, có khả năng làm việc tại các công ty lớn ngay khi ra trường. 
Sinh viên tốt nghiệp có thể vận hành, thiết kế, nâng cấp các hệ thống sản xuất tự động tại các công ty, nhà máy; Giảng dạy, nghiên cứu tại các Viện, các trường Đại học, Cao đẳng, Trung cấp Chuyên nghiệp. Tự động hóa trong sản xuất là một lĩnh vực đang được các nền công nghiệp đặt ra nhiều cơ hội và định hướng phát triển, do đó SV ra trường sẽ có nhiều cơ hội việc làm với mức lương cao.
2. Tổ hợp xét tuyển:
- Tổ hợp A00: Toán, Lý, Hóa.
- Tổ hợp A01: Toán, Lý, Anh.
- Tổ hợp D01: Toán, Văn, Anh.
- Tổ hợp D89: Toán, Anh, Khoa học tự nhiên (KHTN).
điểm chuẩn năm 2024-2025: 28,5d
3. Hotline tư vấn chuyên ngành:
- PGS.TS Vũ Văn Phong - 0981.479.507 - Email: phongvv@hcmute.edu.vn 

- PGS.TS Nguyễn Minh Tâm - Trưởng khoa Điện Điện tử - 0902.873.941 - tamnm@hcmute.edu.vn
"""

IT_STATIC_ANSWER = """
NGÀNH CÔNG NGHỆ THÔNG TIN (7480201V, 7480201A, 7480201N)
KHOA CÔNG NGHỆ THÔNG TIN, TRƯỜNG ĐH SƯ PHẠM KỸ THUẬT TP. HỒ CHÍ MINH
NGÀNH ĐẠT CHUẨN KIỂM ĐỊNH CHẤT LƯỢNG QUỐC TẾ AUN-QA (từ năm 2019)

1. Giới thiệu về ngành:
Trang bị kiến thức khoa học cơ bản, cơ sở và chuyên sâu về các lĩnh vực:
Công nghệ phần mềm, Mạng máy tính và An ninh mạng, Hệ thống thông tin, Trí tuệ nhân tạo.

Ngành CNTT giữ vai trò trọng yếu trong chuyển đổi số, sản xuất thông minh và kinh tế tri thức.
Nhu cầu nhân lực CNTT tại Việt Nam rất lớn, cơ hội việc làm rộng mở trong và ngoài nước.

2. Điều kiện học tập:
Sinh viên học tập trong môi trường hiện đại, hệ thống máy tính và máy chủ mạnh.
Chú trọng thực hành, kỹ năng nghề nghiệp, gắn kết doanh nghiệp.
Tham gia các hoạt động học thuật: Hackathon, Mastering IT, CTF HCMUTE, nghiên cứu khoa học.

3. Cơ hội việc làm:
Kỹ sư phần mềm, kiểm thử phần mềm, quản trị cơ sở dữ liệu, mạng máy tính,
an ninh mạng, AI, hệ thống thông tin.
Có thể nghiên cứu, giảng dạy tại các viện, trường đại học.

4. Tổ hợp xét tuyển:
- A00: Toán – Lý – Hóa
- A01: Toán – Lý – Anh
- D01: Toán – Văn – Anh
- D90: Toán – Anh – KHTN

5. Tư vấn viên:
- PGS.TS Hoàng Văn Dũng – dunghv@hcmute.edu.vn – 0913317759
- TS Huỳnh Xuân Phụng – phunghx@hcmute.edu.vn – 0967853915
"""
TRUONG_STATIC_ANSWER = """1. Lịch sử hình thành và phát triển
Trường Đại học Sư phạm Kỹ thuật TP. Hồ Chí Minh được hình thành và
phát triển trên cơ sở Ban Cao đẳng Sư phạm Kỹ thuật, thành lập ngày 05/10/1962.
Ngày 21/9/1972, Trường được đổi tên thành Trung tâm Cao đẳng Sư phạm
Kỹ thuật Nguyễn Trường Tộ - Thủ Đức.
Năm 1974, Trường được đổi tên thành Trường Đại học Giáo dục Thủ Đức
là 01 trong 07 thành viên của Viện Đại học Bách khoa Thủ Đức.
Ngày 27/10/1976, Thủ tướng Chính phủ ký quyết định thành lập Trường Đại
học Sư phạm Kỹ thuật Thủ Đức trên cơ sở Trường Đại học Giáo dục Thủ Đức.
Năm 1984, Trường sáp nhập với Trường Trung học Công nghiệp Thủ Đức
và đổi tên thành Trường Đại học Sư phạm Kỹ thuật TP. Hồ Chí Minh.
Năm 1991, Trường Sư phạm Kỹ thuật V được sáp nhập vào Trường Đại học
Sư phạm Kỹ thuật TP.HCM.
Từ ngày 27/01/1995, Trường Đại học Sư phạm Kỹ thuật TP.HCM trực thuộc
Đại học Quốc gia.
Theo quyết định số 118/2000/QĐ-TTg ngày 10/10/2000 của Thủ tướng
Chính phủ, Trường Đại học Sư phạm Kỹ thuật TP.HCM được tách khỏi Đại học
Quốc gia và trực thuộc Bộ Giáo dục và Đào tạo.
2. Sứ mệnh
Trường Đại học Sư phạm Kỹ thuật Thành phố Hồ Chí Minh: Cung cấp nguồn
nhân lực chất lượng cao cho thị trường lao động trong nước và quốc tế; Đóng góp
tri thức hữu ích cho nhân loại bằng các kết quả nghiên cứu khoa học nhằm phục
vụ cho sự phát triển bền vững của đất nước; Phục vụ tích cực và có trách nhiệm
vào sự phát triên cộng đồng.
3. Tầm nhìn
Trường Đại học Sư phạm Kỹ thuật Thành phố Hồ Chí Minh là trường Đại
học xuất sắc đa ngành đa lĩnh vực, đổi mới sáng tạo, hội nhập quốc tế và phát
triển bền vững.
4. Triết lý giáo dục: “NHÂN BẢN – SÁNG TẠO – HỘI NHẬP”
5. Giá trị cốt lõi:
Các giá trị cơ bản của một nền giáo dục tiên tiến; hiện đại đã, đang và sẽ
được Trường tôn vinh, gìn giữ, phát huy một cách sáng tạo là:
+ Gìn giữ và phát huy các giá trị truyền thống nhân văn của dân tộc Việt Nam.
+ Nâng đỡ tài năng và tính sáng tạo, chú trọng đào tạo kỹ năng và trách
nhiệm nghề nghiệp.
+ Tôn trọng lợi ích của người học và của cộng đồng. Xây dựng xã hội học tập.
+ Đề cao chất lượng, hiệu quả và sự đổi mới trong các hoạt động.
+ Hội nhập, hợp tác và chia sẻ.
6. Văn hóa chất lượng
Không ngừng nâng cao chất lượng dạy, học, nghiên cứu khoa học nhằm
mang đến cho người học những điều kiện tốt nhất để phát triển toàn diện các năng
lực đáp ứng nhu cầu phát triển và hội nhập quốc tế.
7. Thành tích
- Huân chương Độc lập hạng Nhì (năm 2012),
- Huân chương Độc lập hạng Ba (năm 2007),
- Huân chương Lao động hạng Nhất (năm 2001),
- Huân chương Lao động hạng Nhì (năm 1996),
- Huân chương Lao động hạng Ba (năm 1985).
"""
TKVM_STATIC_ANSWER = """NGÀNH KỸ THUẬT THIẾT KẾ VI MẠCH (7510302KTVM)
KHOA ĐIỆN ĐIỆN TỬ, TRƯỜNG ĐẠI HỌC SƯ PHẠM KỸ THUẬT TP. HỒ CHÍ MINH
1. Giới thiệu về ngành
- Ngành Kỹ thuật thiết kế vi mạch là một ngành đào tạo chuyên sâu trong lĩnh vực kỹ thuật điện tử. Người học trong ngành này được đào tạo để thiết kế và phát triển các vi mạch điện tử, là những hệ thống tích hợp các linh kiện điện tử như transistor, điện trở, tụ điện, và các thành phần khác, trên một nền chất bán dẫn như silic....
- Sinh viên sau khi tốt nghiệp có khả năng làm việc trong lĩnh vực thiết kế và chế tạo vi mạch bản dẫn với khả năng nhận diện và giải quyết các vấn đề quan trọng trong nhiều lĩnh vực ứng dụng khác nhau; có khả năng phát triển sự nghiệp thành công trong công nghiệp, học thuật và phục vụ cộng đồng, thể hiện tinh thần lãnh đạo kỹ thuật trong kinh doanh, nghề nghiệp và cộng đồng; có khả năng tham gia quá trình thúc đẩy sự phát triển kinh tế toàn diện khu vực Miền Nam thông qua việc kết hợp giữa sự thành thạo kỹ thuật, tinh thần lãnh đạo và tinh thần khởi nghiệp. Sinh viên sau khi tốt nghiệp có thể làm việc tại các công ty hoạt động trong lĩnh vực thiết kế và chế tạo vi mạch bán dẫn cũng như các lĩnh vực liên quan khác.
2. Tổ hợp xét tuyển:
- Tổ hợp A00: Toán, Lý, Hóa.
- Tổ hợp A01: Toán, Lý, Anh.
- Tổ hợp D01: Toán, Văn, Anh.
- Tổ hợp C01 : Toán – Văn – Lý.
3. Hotline tư vấn chuyên ngành:
- PGS.TS Võ Minh Huân - 0909.437.522 - Email: huanvm@hcmute.edu.vn 
- PGS.TS Lê Mỹ Hà - Phụ trách Khoa Điện Điện tử - 0938.811.201 - Email: halm@hcmute.edu.vn 
- TS. Phạm Ngọc Sơn - 0966 609 555 - Email: sonpndtvt@hcmute.edu.vn"""
HOSO_STATIC_ANSWER = """HƯỚNG DẪN THỰC HIỆN THỦ TỤC HỒ SƠ NHẬP HỌC
Bước 1: Tân sinh viên truy cập vào website https://nhaphoc.hcmute.edu.vn/ , đăng nhập bằng tài
khoản mà nhà trường đã gửi qua tin nhắn SMS hoặc xem trên trang tra cứu kết quả xét tuyển
https://tracuuxettuyen.hcmute.edu.vn/ và chuẩn bị đầy đủ thông tin để điền và tải ảnh lên hệ thống.
Lưu ý: phải điền đúng mật khẩu bao gồm phần chữ và phần số (Ví dụ: SPK&12345678)
Bước 2: Chọn “Bước 1 – Hồ sơ sinh viên”, sau đó thực hiện điền đầy đủ các ô thông tin
Lưu ý:
– Phần nơi sinh, quê quán: chọn chính xác tỉnh/thành phố theo thông tin được ghi trên giấy khai
sinh.
– Phần Mã số BHYT: điền đủ 15 ký tự cả phần chữ và số (ví dụ: HS 4 79 512 137 4007)
– Phần thời gian tham gia BHYT, mã nơi đăng ký Khám chữa bệnh ban đầu, Tên nơi đăng ký
Khám chữa bệnh ban đầu, sinh viên điền đúng nội dung trên app VSSID, hoặc tra cứu trên
https://baohiemxahoi.gov.vn/tracuu/Pages/tra-cuu-thoi-han-su-dung-the-bhyt.aspx– Nếu sinh viên là Đoàn viên/Đảng viên, phải tick vào và ghi đủ ngày kết nạp và nơi kết nạp.
Nếu không phải Đoàn viên/Đảng viên thì không tick.
– Phần Tên chức vụ Đoàn-Hội-Lớp: có thể ghi “không có” nếu không giữ chức vụ nào.
Sau khi điền đầy đủ các ô thông tin, sinh viên bấm “Lưu thông tin” ở cuối trang.
Nên nhập nhanh các thông tin ở bước này, tránh treo web quá lâu sẽ bị mất kết nối và lưu sẽ
không thành công.
Bước 3: Chọn “Bước 2 – danh sách file đính kèm” và chuẩn bị trước ảnh các giấy tờ mà trường
yêu cầu nộp ở bước này.
File ảnh tải lên và bấm lưu thành công 
Sinh viên nên tải lên từng ảnh xong bấm lưu hồ sơ ở cuối trang, rồi mới tải lên tiếp các ảnh
tiếp theo, tránh để web treo quá lâu dẫn đến lỗi.
Lưu ý:
– Các giấy tờ phải chụp bản gốc hoặc bản photo công chứng.
– Đối với thí sinh tốt nghiệp năm 2025, phải tải lên giấy chứng nhận tốt nghiệp tạm thời, không
tải lên ảnh ở mục bằng tốt nghiệp THPT.
 Đối với thí sinh tốt nghiệp năm 2024 trở về trước, chỉ tải lên bằng tốt nghiệp THPT.
 hình thẻ 4x6 chỉ được tải lên file JPG và file PNG phải crop gọn ảnh trước khi tải lên.
 Các trang học bạ phải tải lên theo đúng thứ tự các trang.
 Kích thước file không được quá lớn, nếu tải ảnh lên bị lỗi thì phải kiểm tra lại kích thước ảnh.
Bước 4: Chọn và xem học phí ở “Bước 3 – Tình trạng học phí nhập học”. Sinh viên truy cập trang
web http://fpo.hcmute.edu.vn/ để xem hướng dẫn cách thanh toán học phí online. Và thanh toán
học phí online tại https://e-bills.vn/pay/hcmute. Mọi thắc mắc về tiền học phí trong thời gian
nhập học, sinh viên vui lòng liên hệ hotline 0947799617 hoặc 0931141206 trong giờ hành
chính.
Sau 24 giờ sau khi hoàn thành 3 bước trên, tân sinh viên thường xuyên vào lại theo dõi tình
trạng hồ sơ và học phí. Nếu hồ sơ được duyệt (hoặc có sai sót) sẽ có thông báo ở đầu trang.
Bước 5: Sinh viên xác nhận nhập học trên web thisinh.thithptquocgia.edu.vn (trước 17h ngày
30/8/2025). Nếu đã xác nhận, vui lòng đợi từ 24h - 48h để được cập nhật ở “Bước 4 - Xác nhận
nhập học bằng phiếu điểm thi THPT”.
Sau khi hoàn thành các bước trên: Tân sinh viên chọn “Bước 0 – Các thông báo cho việc nhập học”
để xem qua các thông báo cần thiết và quan trọng.
Mọi thắc mắc, vấn đề về thủ tục nhập học, tân sinh viên vui lòng liên hệ qua số điện thoại
02837222764 vào giờ hành chính, hoặc liên hệ qua fanpage https://www.facebook.com/ute.sao,
https://www.facebook.com/SPKT.tuyensinh, https://www.facebook.com/share/g/172wq5ybNp/
để được hỗ trợ kịp thời."""
NNANH_STATIC_ANSWER = """NGÀNH NGÔN NGỮ ANH (7220201V)
KHOA NGOẠI NGỮ, TRƯỜNG ĐẠI HỌC SƯ PHẠM KỸ THUẬT TP. HỒ CHÍ MINH
1. Giới thiệu về Ngành gồm 02 chương trình: Biên Phiên dịch và Tiếng Anh Thương mại
1.1. Chương trình: Biên Phiên dịch
- Chương trình Biên Phiên dịch trang bị cho người học những kiến thức về khoa học xã hội, khoa học tự nhiên và hệ thống kiến thức về ngành Biên - Phiên dịch Tiếng Anh Kỹ thuật. Từ đó, người học có khả năng sử dụng tốt các kỹ năng tiếng Anh và thuật ngữ để chuyển ngữ giữa tiếng Anh và tiếng Việt trong các lĩnh vực kỹ thuật. Người hoàn thành chương trình đào tạo có khả năng thu thập, phân tích và sàng lọc thông tin cũng như ứng dụng tri thức mới vào thực tiễn hoạt động biên phiên dịch.
- Cử nhân ngành Biên Phiên dịch được trang bị kiến thức, kỹ năng nghề nghiệp, và phẩm chất đạo đức tốt để có thể làm việc hiệu quả trong các lĩnh vực liên quan đến hoạt động biên phiên dịch, đáp ứng được yêu cầu của xã hội và của nền kinh tế trong quá trình hội nhập quốc tế.
1.2. Chương trình: Tiếng Anh Thương mại
- Chương trình Tiếng Anh Thương mại trang bị cho người học những kiến thức về khoa học xã hội, khoa học tự nhiên, hệ thống kiến thức về ngành Tiếng Anh Thương mại và kỹ năng nghề nghiệp. Từ đó, người học có khả năng sử dụng tốt các kỹ năng tiếng Anh và kiến thức cần thiết về thương mại để có thể làm việc hiệu quả trong các lĩnh vực liên quan đến hoạt động thương mại tại các tổ chức và doanh nghiệp ở Việt nam và quốc tế.
- Sự xuất hiện ngày càng nhiều của các nhà đầu tư nước ngoài đã thúc đẩy sự gia tăng các nhu cầu về nhân lực có trình độ Tiếng Anh, đặc biệt là Tiếng Anh trong lĩnh vực kinh tế. Vì vậy, Tiếng Anh Thương Mại lại được xem ngôn ngữ của thời hội nhập.
2. Điều kiện học tập và rèn luyện của sinh viên
- Đội ngũ giảng viên được đánh giá cao về trình độ chuyên môn và kinh nghiệm giảng dạy. Giảng viên sẽ hỗ trợ sinh viên hiểu rõ và ứng dụng kiến thức vào môi trường dịch thuật một cách hiệu quả.
- Khoa Ngoại ngữ có các phòng học hiện đại với trang thiết bị như máy chiếu, máy tính, TV LCD, và đặc biệt là phòng dịch CABIN chuyên biệt, tạo điều kiện tốt cho việc thực hành kỹ năng phiên dịch.
- Thư viện đồ sộ với hàng ngàn tài liệu chuyên ngành trong và ngoài nước, cùng với các phần mềm dịch thuật và công cụ hỗ trợ, giúp sinh viên nghiên cứu sâu hơn về ngành nghề.
- Mạng lưới cựu sinh viên đặc biệt quan trọng, giúp sinh viên tiếp cận kinh nghiệm học tập và sự nghiệp từ những người đã thành công trong lĩnh vực biên phiên dịch kỹ thuật.
- Mối quan hệ mạnh mẽ với doanh nghiệp giúp sinh viên có cơ hội thực tập và tuyển dụng sau khi tốt nghiệp. Các buổi đối thoại giữa sinh viên và chuyên gia trong lĩnh vực biên phiên dịch tạo cơ hội trao đổi thông tin và nắm bắt xu hướng thị trường.
- Các hoạt động ngoại khóa như giao lưu văn hóa, tham quan, dã ngoại, cùng với các câu lạc bộ như Step-up và câu lạc bộ dịch thuật giúp sinh viên phát triển kỹ năng và tiếng Anh, cũng như kỹ năng biên phiên dịch. Gala Night và các sự kiện khác tạo cơ hội cho sinh viên thể hiện tài năng và tận hưởng không khí văn hóa nghệ thuật.
- Trong các khóa học, sinh viên có nhiều cơ hội trải nghiệm luyện tập kỹ năng và ứng dụng kiến thức trong bối cảnh môi trường thương mại. Ví dụ như: ứng dụng kỹ năng và kiến thức trong các tình huống giao tiếp đa văn hóa, đàm phán kinh doanh, giao dịch thư từ, soạn thảo hợp đồng Thương mại quốc tế và các tình huống liên quan đến vấn đề nhân sự, giao dịch thương mại đện tử và nghiên cứu thị trường.
- Sinh viên được học dưới sự hướng dẫn của các thầy cô có trình độ chuyên môn cao với phương pháp giảng dạy hiệu quả, sáng tạo, lấy người học làm trung tâm.
- Sinh viên được tạo điều kiện tham gia các buổi giao lưu với các chuyên gia đến từ các doanh nghiệp, được trao đổi, học hỏi nhiều kinh nghiệm thực tế.
3. Cơ hội việc làm sau khi tốt nghiệp của sinh viên
- Các doanh nghiệp thường tuyển dụng: Cơ quan, công ty, doanh nghiệp, báo đài và các tổ chức xã hội trong và ngoài nước, các công ty đa quốc gia, các công ty Việt Nam có đối tác là các công ty nước ngoài, …
- Những vị trí sinh viên có thể ứng tuyển
+ Biên phiên dịch chuyên nghiệp cho các cơ quan, doanh nghiệp, báo đài và các tổ chức trong và ngoài nước. Ngoài ra, sinh viên sau khi tốt nghiệp cũng có thể làm các công việc liên quan khác như thư ký, trợ lý, hướng dẫn viên du lịch, tiếp viên hàng không hoặc giảng dạy tiếng Anh. Đặc biệt, cư nhân Biên Phiên dịch sẽ được phát huy các năng lực cá nhân để có thể tự học hiệu quả và tiếp tục nghiên cứu ở các bậc học cao hơn.
- Cử nhân tiếng anh thương mại có thể ứng tuyển vào các vị trí bán hàng, giao dịch viên, nhân sự, truyền thông, đối ngoại, thư ký, trợ lý, phiên dịch và quản lý các cấp trong các công ty, tổ chức về thương mại, ngân hàng, xuất nhập khẩu của Việt nam và quốc tế. Ngoài ra, với lợi thế về trình độ tiếng Anh, nếu được bồi dưỡng thêm về nghiệp vụ sư phạm, các cử nhân tiếng Anh thương mại cũng có thể đảm nhận công tác giảng dạy Tiếng Anh chuyên ngành tại các cơ sở đào tạo khác nhau.
4. Chương trình được xét tuyển với một trong hai tổ hợp môn sau:
- Tổ hợp D01: Toán, Văn, tiếng Anh*
- Tổ hợp D96: Toán, tiếng Anh*, KHXH (Sử - Địa - GDCD)
* Điểm tiếng Anh nhân hệ số 2
5. Các tư vấn viên hướng nghiệp về Chương trình:
- Lê Phương Anh - 0989 071 934 - anhlp@hcmute.edu.vn
- Phạm Văn Khanh - 0934 285 007 - khanhpv@ hcmute.edu.vn
- Huỳnh Hạnh Dung - 0982110210 - dunghh@hcmute.edu.vn
- Lê Thị Thanh Hà - 0908164441- thanhha@hcmute.edu.vn"""
KTHH_STATIC_ANSWER = """NGÀNH CÔNG NGHỆ KỸ THUẬT HÓA HỌC (7510401V)
KHOA CÔNG NGHỆ HÓA HỌC VÀ THỰC PHẨM, TRƯỜNG ĐH SƯ PHẠM KỸ THUẬT TP.HCM
NGÀNH ĐẠT CHUẨN KIỂM ĐỊNH CHẤT LƯỢNG QUỐC TẾ AUN-QA (từ năm 2022
1. Giới thiệu về ngành Công nghệ kỹ thuật Hóa học (Chemical Engineering Technology): là ngành khoa học kỹ thuật dựa trên nền tảng các kiến thức của khoa học Hóa học để từ đó nghiên cứu phát triển, thiết kế và vận hành các công nghệ sản xuất những sản phẩm thuộc lĩnh vực Hóa học. Đây là một ngành khoa học kỹ thuật kết hợp các kiến thức của Hóa học cơ bản và Hóa học công nghệ.
Ngành CNKT Hóa học là một ngành công nghệ chủ chốt của nền công nghiệp và sản xuất Việt Nam. Do đó, cả hiện tại và tương lai, ngành CNKT Hóa học là một ngành học quan trọng và cung cấp cho xã hội một lực lượng lớn Kỹ sư Hóa đáp ứng nhu cầu phát triển kinh tế xã hội.
2. Điều kiện học tập và rèn luyện của sinh viê
Ngành CNKT Hóa học sẽ trang bị cho sinh viên những kiến thức từ cơ bản đến nâng cao trong lĩnh vực Kỹ thuật Hóa học, cung cấp những kỹ năng cần thiết để làm việc trong phòng thí nghiệm và làm việc như một Kỹ sư công nghệ tại các đơn vị sản xuất kinh doanh trong lĩnh vực công nghiệp Hóa học. Sinh viên tốt nghiệp sẽ có những kiến thức về qui trình sản xuất, các bước chuyển hóa của hóa chất trong công nghệ sản xuất, tính toán thiết kế, lập bản vẽ, đọc bản vẽ thiết kế, vận hành máy móc, cách thức kiểm soát và cải tiến qui trình công nghệ, các phương pháp đánh giá tính chất của sản phẩm…
Chương trình đào tạo cũng cung cấp cho sinh viên những kiến thức chuyên sâu về lý thuyết và công nghệ sản xuất của một trong 4 chuyên ngành hẹp, bao gồm:
- CNKT Hóa hữu cơ: tập trung đào tạo Kỹ sư về công nghệ chiết tách các hợp chất thiên nhiên, công nghệ sản xuất các hương liệu, mỹ phẩm và các sản phẩm chăm sóc cá nhân, công nghệ sản xuất giấy, công nghệ sản xuất các chất màu hữu cơ, công nghệ nhuộm màu…
- CNKT Hóa vô cơ: tập trung đào tạo Kỹ sư về công nghệ sản xuất phân bón; công nghệ sản xuất xi măng, gạch ngói và gốm sứ; công nghệ sản xuất thủy tinh; công nghệ sản xuất các sản phẩm điện hóa (pin, acquy…) và các công nghệ xi mạ…
- CNKT Hóa Polymer: tập trung đào tạo Kỹ sư về công nghệ sản xuất chất dẻo tổng hợp, công nghệ gia công các sản phẩm Polymer (đùn, đúc, ép…), công nghệ cao su thiên nhiên và cao su tổng hợp, công nghệ vật liệu Composite, công nghệ sản xuất Sơn và các chất kết dính (keo)…
- CNKT Hóa Dược: tập trung đào tạo Kỹ sư về công nghệ chiết tách các hợp chất thiên nhiên có dược tính, kỹ thuật tổng hợp, thiết kế thuốc và kiểm định thuốc, kỹ thuật đánh giá hoạt tính sinh học của thuốc, công nghệ cơ bản trong lĩnh vực gia công và sản xuất các dạng thuốc viên, thuốc cốm, thuốc nước… Ngoài ra, chương trình cũng sẽ cung cấp các kiến thức cơ bản về công nghệ sản xuất kháng sinh, vaccine và thực phẩm chức năng.
Chương trình đào tạo đặc biệt chú trọng tăng cường các môn học thực hành, thí nghiệm và kết hợp đào tạo thực tế tại các doanh nghiệp. SV có cơ hội tiếp cận với các trang thiết bị thí nghiệm hiện đại cùng với các máy móc phân tích kỹ thuật cao.
Chương trình đào tạo cũng chú trọng các kiến thức bổ trợ giúp đào tạo được một Kỹ sư có kiến thức toàn diện để đáp ứng được nhu cầu nguồn nhân lực ngày càng cao của thị trường lao động và của toàn xã hội như: Kinh tế học, Quản trị học, Tối ưu hóa và khối kiến thức về Công nghệ thông tin…
SV được hướng dẫn học tập bởi một lực lượng giảng viên có trình độ cao (100% giảng viên các môn cơ sở ngành và chuyên ngành có trình độ Tiến sĩ).
3. Cơ hội việc làm sau khi tốt nghiệp của sinh viên
Sau khi tốt nghiệp, Kỹ sư ngành CNKT Hóa học có thể hoạt động và làm việc tại các vị trí sau:
· Cán bộ giảng dạy ngành Hóa học và CNKT Hóa học tại các trường đại học và cao đẳng;
· Có thể tiếp tục học sau đại học (thạc sỹ, tiến sỹ): để trở thành các chuyên gia và cán bộ nghiên cứu.
· Cán bộ nghiên cứu và phát triển sản phẩm trong các viện, các trung tâm, các công ty, các nhà máy xí nghiệp sản xuất các sản phẩm Hóa học.
· Kỹ sư công nghệ quản lý sản xuất tại bộ phận Kỹ thuật trong các công ty sản xuất
· Chuyên viên kế hoạch sản xuất
· Chuyên viên đảm bảo chất lượng (QA)
· Chuyên viên kiểm soát chất lượng (QC)
· Chuyên viên kinh doanh các sản phẩm, trang thiết bị, công nghệ Hóa học
4. Ngành được xét tuyển với các tổ hợp môn
- A00 (Toán, Lý, Hóa)
- B00 (Toán, Hóa, Sinh)
- D90 (Toán, KHTN, Anh)
- D07 (Toán, Hóa, Anh)
5. Các tư vấn viên hướng nghiệp về ngành
- TS. Nguyễn Thị Tịnh Ấu (SĐT: 0909 098 536)
- TS. Huỳnh Nguyễn Anh Tuấn (SĐT: 0933 735 364)"""
TKDH_STATIC_ANSWER = """NGÀNH THIẾT KẾ ĐỒ HỌA (7210403V)
KHOA IN VÀ TRUYỀN THÔNG, TRƯỜNG ĐẠI HỌC SƯ PHẠM KỸ THUẬT TP. HỒ CHÍ MINH
1. Giới thiệu về ngành:
-  Thiết kế đồ họa là ngành học kết hợp giữa ý tưởng sáng tạo và khả năng cảm nhận thẩm mỹ, thông qua các công cụ đồ họa để truyền tải thông điệp bằng những hình ảnh đẹp, ấn tượng… Nói cách khác Đồ họa là sự kết hợp giữa nghệ thuật và thông tin. Thiết kế đồ họa là loại hình nghệ thuật ứng dụng, kết hợp hình ảnh chữ viết và ý tưởng một cách sáng tạo để truyền đạt thông tin hiệu quả và thú vị qua các hình thức ấn phẩm in ấn và trực tuyến.
- Với sự phát triển của công nghệ, đặc biệt là công nghệ 3D, ngành thiết kế đồ họa đang tiến xa hơn và trở thành một lĩnh vực đầy triển vọng trong tương lai. Công nghệ thực tế ảo (VR) và thực tế tăng cường (AR) đã mở ra nhiều cơ hội mới cho các nhà thiết kế đồ họa. Nhờ vào những công nghệ này, người ta có thể tạo ra những trải nghiệm tương tác đáng kinh ngạc và đưa người dùng vào một thế giới sống động, chân thực.
- Bên cạnh đó, các xu hướng thiết kế đồ họa như đồ họa động, thiết kế đa phương tiện và thiết kế trải nghiệm người dùng (UX, UI) cũng đang ngày càng được chú trọng. Tầm quan trọng của việc tạo ra những sản phẩm tương tác và dễ sử dụng ngày càng được nhận ra, đặc biệt là trong lĩnh vực tiếp thị và truyền thông.
2. Điều kiện học tập và rèn luyện của sinh viên
- Sinh viên được trang bị kiến thức, kỹ năng về nền tảng nghệ thuật và phương pháp thiết kế, các kỹ thuật ứng dụng và sử dụng công nghệ trong thiết kế đồ họa, xu hướng phát triển các ứng dụng đồ họa trên thế giới,... Sinh viên tốt nghiệp có khả năng kết hợp giữa thiết kế với truyền thông, mỹ thuật, thương mại để đáp ứng tốt những yêu cầu của nền công nghiệp sáng tạo và giải trí hiện đại, phát triển các kỹ năng chuyên môn như: kỹ năng sáng tác và thể hiện, kỹ năng nắm bắt tâm lý khách hàng, kỹ năng làm việc nhóm, kỹ năng làm việc độc lập, kỹ năng đàm phán, kỹ năng lãnh đạo,...
- Sinh viên được học dưới sự hướng dẫn của các thầy cô giàu kinh nghiệm giảng dạy và làm việc trong ngành, cùng với lực lượng giảng viên trẻ tận tậm.
- Thông qua việc hợp tác của khoa với các Doanh nghiệp, sinh viên luôn được tạo điều kiện tham gia các học kỳ doanh nghiệp, được tham quan trực tiếp, cũng như liên kết kiến tập, thực tập tại các công ty trong và ngoài nước. Đồng thời tạo điều kiện thuận lợi về việc làm sau khi ra trường cho sinh viên.
- Bên cạnh đó sinh viên còn được tham gia các hoạt động sáng tạo, xây dựng và phát triển kỹ năng cá nhân thông qua các hoạt động CLB Nghiên cứu khoa học, CLB Kỹ năng, CLB Ghita, CLB Sáng tạo khởi nghiệp….
3. Cơ hội việc làm sau khi tốt nghiệp của sinh viên
- Ví dụ những vị trí sinh viên có thể ứng tuyển
Cơ hội nghề nghiệp dành cho các Cử nhân tốt nghiệp ngành Thiết kế đồ họa có thể kể đến như sau: chuyên viên thiết kế, tư vấn thiết kế tại các công ty quảng cáo, công ty thiết kế, công ty truyền thông và tổ chức sự kiện, studio nghệ thuật, xưởng phim hoạt hình và truyện tranh, các tòa soạn, các nhà xuất bản, cơ quan truyền hình, báo chí,... Ngoài ra, sau khi tốt nghiệp, sinh viên có thể tự thành lập doanh nghiệp, các công ty thiết kế, dịch vụ studio hoặc tư vấn, giảng dạy tại các trường học, trung tâm, CLB,... Hơn nữa, như một đặc thù ưu ái, ngành Thiết kế đồ họa luôn mang lại những cơ hội làm thêm hấp dẫn tại nhà như thiết kế website, thiết kế logo, nhận diện thương hiệu,...
Một số vị trí việc làm:
· Nhân viên thiết kế bộ phận Marketing
· Nhân viên thiết kế đồ hoạ truyền thông
· Nhân viên tại các studio
· Tư vấn viên thiết kế
· Chỉ đạo sáng tạo
· Nghiên cứu thông tin, dữ liệu xây dựng concept sản phẩm
· Giám sát chất lượng, đảm bảo thiết kế
4. Ngành được xét tuyển với các tổ hợp môn
- V01 (Toán - Văn - Vẽ TT)
- V02 (Toán - Anh - Vẽ TT)
- V07 (Văn - Vẽ ĐT - Vẽ TT)
- V08 (Văn - Anh - Vẽ TT)
5. Các tư vấn viên hướng nghiệp về ngành
- TS. Nguyễn Long Giang – Trưởng khoa In và Truyền thông - 0903.678.610
- Ths. Lê Công Danh – Phó Trưởng khoa In và Truyền thông - 0903.344.837
- Ths. Vũ Trần Mai Trâm - Giảng viên ngành Thiết kế Đồ họa - 0902.996.092
- Ths. Vũ Ngàn Thương - Giảng viên ngành Thiết kế Đồ họa - 0377.410.810"""
def search(query, k=10):
    query_lower = query.lower()
    kthh_keywords =[
        "ngành kỹ thuật hóa học là gì",
        "công nghệ kỹ thuật hóa học",
        "kthh",
        "kỹ thuật hóa học",
        "thông tin về ngành kỹ thuật hóa học",
    ]
    tkvm_keywords = [
        "thiết kế vi mạch",
        "giới thiệu về thiết kế vi mạch",
        "giới thiệu về ngành thiết kế vi mạch",
        "ngành thiết kế vi mạch",
        "ngành thết kế vi mạch là gì",
        "thiết kế vi mạch là gì",
        "tkvm là gì",
        "tkvm"
    ]
    tkdh_keywords = [
        "thiết kế đồ họa là gì",
        "ngành thiết kế đồ họa",
        "giới thiệu về ngành thiết kế đồ họa",
        "tkdh",
        "thiết kế đồ họa"
    ]
    nnanh_keywords = [
        "ngành ngôn ngữ anh là gì",
        "ngôn ngữ anh",
        "ngành ngôn ngữ anh",
        "English language"
    ]
    automation_keywords = [
        "tự động hóa",
        "ngành tự động hóa",
        "automation",
        "ngành automation",
        "điều khiển và tự động hóa"
    ]
    it_keywords = [
        "công nghệ thông tin",
        "ngành công nghệ thông tin",
        "cntt",
        "it",
        "information technology"
    ]
    truong_keywords = [
        "giới thiệu về trường",
        "lịch sử hình thành trường",
        "đại học sư phạm kỹ thuật",
        "đại học công nghệ kỹ thuật",
        "ute",
        "hcmute",
        "lịch sử hình thành của trường",
        "giới thiệu trường",
        "giới thiệu về trường đại học sư phạm kỹ thuật",
        "giới thiệu về trường công nghệ kỹ thuật",
    ]
    hoso_keywords = [
        "hướng dẫn thực hiện hồ sơ nhập học",
        "hồ sơ nhâp học làm sao",
        "cách làm hồ sơ nhập học",
        "khi biết điểm rồi thì hồ sơ làm sao",
        "hồ sơ"
    ]
    if any(kw in query_lower for kw in automation_keywords):
        return "AUTOMATION_STATIC"
    if any(kw in query_lower for kw in tkvm_keywords):
        return "TKVM_STATIC"
    if any(kw in query_lower for kw in kthh_keywords):
        return "KTHH_STATIC"
    if any(kw in query_lower for kw in it_keywords):
        return "IT_STATIC"
    if any(kw in query_lower for kw in truong_keywords):
        return "TRUONG_STATIC"
    if any(kw in query_lower for kw in hoso_keywords):
        return "HOSO_STATIC"
    if any(kw in query_lower for kw in nnanh_keywords):
        return "NNANH_STATIC"
    if any(kw in query_lower for kw in tkdh_keywords):
        return "TKDH_STATIC"
    embedding = get_embedding_model()
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding
    )
    docs_and_scores = db.similarity_search_with_relevance_scores(query, k=k)
    if not docs_and_scores or docs_and_scores[0][1] < 0.4:
        return "NGOAI_PHAM_VI"
    docs = [doc for doc, score in docs_and_scores]
    keyword_map = {
        "tự động": ["tự động", "tự động hóa", "automation"],
        "điện": ["điện", "điện tử"],
        "nhiệt": ["nhiệt", "điện lạnh"],
        "cơ khí": ["cơ khí", "chế tạo máy", "cnc"],
        "cntt": ["công nghệ thông tin", "cntt", "it", "phần mềm"]
    }
    matched_docs = []
    for doc in docs:
        content = doc.page_content.lower()
        for key, keywords in keyword_map.items():
            if key in query_lower:
                if any(k in content for k in keywords):
                    matched_docs.append(doc)
    if matched_docs:
        return matched_docs[:2]
    return docs[:1]

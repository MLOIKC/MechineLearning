function vdm=VDM(a,b,C,u,p)
% VDM计算属性u上两个离散值a与b之间的VDM距离
% C为簇集合，u为属性所在列号，p为距离选择
vdm=0;
[~,~,k]=size(C);

% m_u_a(b)表示属性u上取值为a(b)的样本数
m_u_a=length(find(C(:,u,:)==a));
m_u_b=length(find(C(:,u,:)==b));

for i=1:k
    m_u_a_i=length(find(C(:,u,i)==a));
    m_u_b_i=length(find(C(:,u,i)==b));
    vdm=vdm+(abs((m_u_a_i/m_u_a)-(m_u_b_i/m_u_b)))^p;
end
